"""Model-agnostic LLM layer.

Every provider is reached through the OpenAI-compatible Chat Completions API,
so swapping models = changing LLM_PROVIDER / LLM_MODEL (env or sidebar).
Nothing else in the app knows which vendor is behind it.
"""
from __future__ import annotations

import base64
import json
import os
import re
import threading
import time
from dataclasses import dataclass

from openai import OpenAI

PRESETS: dict[str, dict] = {
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "key_env": "GEMINI_API_KEY",
        "model": "gemini-3.5-flash",
        "vision_model": None,          # same model handles images
        "stt": "chat_audio",           # audio sent inline to the chat model
        "stt_model": None,
        "rpm": 5,                      # free tier: 5 requests/min PER MODEL
        "fallback_models": ["gemini-3.5-flash-lite", "gemini-flash-lite-latest"],  # separate quotas
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "key_env": "GROQ_API_KEY",
        "model": "openai/gpt-oss-120b",
        "rpm": 30,
        "vision_model": "qwen/qwen3.8-27b",
        "stt": "whisper",
        "stt_model": "whisper-large-v3-turbo",
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "key_env": "OPENROUTER_API_KEY",
        "model": "google/gemini-2.5-flash",
        "vision_model": None,
        "stt": "chat_audio",
        "stt_model": None,
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "key_env": "OPENAI_API_KEY",
        "model": "gpt-4o-mini",
        "vision_model": None,
        "stt": "whisper",
        "stt_model": "whisper-1",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "key_env": "OLLAMA_API_KEY",
        "model": "llama3.1",
        "vision_model": None,
        "stt": "none",
        "stt_model": None,
    },
    # Any other OpenAI-compatible endpoint (e.g. an API Kuku provides):
    # set LLM_BASE_URL, LLM_API_KEY, LLM_MODEL.
    "custom": {
        "base_url": None,
        "key_env": "LLM_API_KEY",
        "model": None,
        "vision_model": None,
        "stt": "chat_audio",
        "stt_model": None,
    },
}


class LLMError(RuntimeError):
    pass


class _RateBook:
    """Process-wide per-model request log, so the app stays under free-tier per-minute caps
    and skips a model that the provider told us to back off from."""

    def __init__(self):
        self.calls: dict[str, list[float]] = {}
        self.cool_until: dict[str, float] = {}
        self.lock = threading.Lock()

    def _recent(self, m):
        now = time.time()
        self.calls[m] = [t for t in self.calls.get(m, []) if now - t < 60]
        return self.calls[m]

    def available(self, m, rpm):
        with self.lock:
            if self.cool_until.get(m, 0) > time.time():
                return False
            return not rpm or len(self._recent(m)) < rpm

    def next_free(self, m, rpm):
        with self.lock:
            t = self.cool_until.get(m, 0)
            rec = self._recent(m)
            if rpm and len(rec) >= rpm:
                t = max(t, rec[0] + 60)
            return t

    def record(self, m):
        with self.lock:
            self.calls.setdefault(m, []).append(time.time())

    def cool(self, m, seconds):
        with self.lock:
            self.cool_until[m] = time.time() + seconds


_RATE = _RateBook()


@dataclass
class LLM:
    provider: str
    model: str
    vision_model: str
    base_url: str
    api_key: str
    stt: str
    stt_model: str | None

    @classmethod
    def from_env(cls, provider: str | None = None, model: str | None = None) -> "LLM":
        provider = (provider or os.getenv("LLM_PROVIDER") or "gemini").lower()
        if provider not in PRESETS:
            raise LLMError(f"Unknown provider '{provider}'. Options: {', '.join(PRESETS)}")
        p = PRESETS[provider]
        base_url = os.getenv("LLM_BASE_URL") if provider == "custom" else p["base_url"]
        key = os.getenv(p["key_env"]) or os.getenv("LLM_API_KEY") or ("ollama" if provider == "ollama" else "")
        model = model or os.getenv("LLM_MODEL") or p["model"]
        if not base_url or not model:
            raise LLMError("Custom provider needs LLM_BASE_URL and LLM_MODEL.")
        vision = os.getenv("LLM_VISION_MODEL") or p["vision_model"] or model
        return cls(provider, model, vision, base_url, key, p["stt"], p["stt_model"])

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def _client(self) -> OpenAI:
        if not self.api_key:
            raise LLMError(
                f"No API key for '{self.provider}'. Set {PRESETS[self.provider]['key_env']} in .env "
                "(or Streamlit secrets)."
            )
        return OpenAI(base_url=self.base_url, api_key=self.api_key, timeout=120)

    # ---------- core call: throttle + rate-limit handling + model fallback ----------
    def _candidates(self, model: str | None) -> list[str]:
        primary = model or self.model
        if primary not in (self.model, self.vision_model):
            return [primary]
        env = os.getenv("LLM_FALLBACK_MODELS")
        fallbacks = [m.strip() for m in env.split(",") if m.strip()] if env is not None else PRESETS[self.provider].get("fallback_models", [])
        return [primary] + [m for m in fallbacks if m != primary]

    def _rpm(self) -> int:
        return int(os.getenv("LLM_RPM") or PRESETS[self.provider].get("rpm") or 0)

    def _complete(self, messages, model=None, temperature=0.3, json_mode=False, max_tokens=None, max_wait=150) -> str:
        models = self._candidates(model)
        base = dict(messages=messages, temperature=temperature)
        if json_mode:
            base["response_format"] = {"type": "json_object"}
        if max_tokens:
            base["max_tokens"] = max_tokens
        deadline = time.time() + max_wait
        last_err = None
        while time.time() < deadline:
            # pick the first model that is not cooling down and has room in its per-minute window
            ready = [m for m in models if _RATE.available(m, self._rpm())]
            if not ready:
                time.sleep(max(0.5, min(_RATE.next_free(m, self._rpm()) for m in models) - time.time()))
                continue
            m = ready[0]
            _RATE.record(m)
            try:
                resp = self._client().chat.completions.create(model=m, **base)
                self.last_model = m
                return (resp.choices[0].message.content or "").strip()
            except Exception as e:  # noqa: BLE001 - surface any provider error
                last_err = e
                body = getattr(getattr(e, "response", None), "text", "") or ""
                msg = f"{e} {body}"
                if json_mode and "response_format" in base and ("response_format" in msg or "json_object" in msg):
                    base.pop("response_format")  # provider lacks JSON mode
                    continue
                if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                    wait = re.search(r"retry in ([\d.]+)s", msg)
                    _RATE.cool(m, float(wait.group(1)) + 1 if wait else 30)
                    continue  # next model, or wait for the soonest one
                if "503" in msg or "overloaded" in msg.lower() or "UNAVAILABLE" in msg:
                    _RATE.cool(m, 5)
                    continue
                break
        raise LLMError(f"{self.provider}/{models[0]} failed: {str(last_err)[:300] if last_err else 'rate limit wait exceeded'}")

    def chat(self, messages, temperature=0.3, max_tokens=None) -> str:
        return self._complete(messages, temperature=temperature, max_tokens=max_tokens)

    def chat_json(self, messages, temperature=0.1, model=None) -> dict:
        text = self._complete(messages, model=model, temperature=temperature, json_mode=True)
        try:
            return parse_json(text)
        except ValueError:
            repair = messages + [
                {"role": "assistant", "content": text},
                {"role": "user", "content": "That was not valid JSON. Reply with ONLY the corrected JSON object."},
            ]
            return parse_json(self._complete(repair, model=model, temperature=0, json_mode=True))

    # ---------- multimodal ----------
    def image_json(self, prompt: str, image_bytes: bytes, mime: str) -> dict:
        b64 = base64.b64encode(image_bytes).decode()
        messages = [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
            ],
        }]
        return self.chat_json(messages, model=self.vision_model)

    def transcribe(self, audio_bytes: bytes, filename: str = "audio.wav") -> str:
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "wav"
        if self.stt == "whisper":
            resp = self._client().audio.transcriptions.create(
                model=self.stt_model, file=(filename, audio_bytes)
            )
            return resp.text.strip()
        if self.stt == "chat_audio":
            fmt = ext if ext in ("wav", "mp3") else "mp3"
            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": (
                        "Transcribe this audio verbatim in the language/script it is spoken in "
                        "(Hinglish stays in Roman script). If there are multiple speakers, label them "
                        "Speaker 1, Speaker 2. Output only the transcript."
                    )},
                    {"type": "input_audio", "input_audio": {"data": base64.b64encode(audio_bytes).decode(), "format": fmt}},
                ],
            }]
            return self._complete(messages, temperature=0)
        raise LLMError(f"Provider '{self.provider}' has no speech-to-text configured; type instead.")


def parse_json(text: str) -> dict:
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if fence:
        text = fence.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                pass
    raise ValueError("Model did not return valid JSON")
