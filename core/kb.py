"""Verified legal knowledge base + citation validator (the anti-hallucination layer)."""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

KB_PATH = Path(__file__).resolve().parent.parent / "kb" / "legal_kb.json"

REPEALED = re.compile(
    r"\b(IPC|I\.P\.C\.?|Indian Penal Code|Cr\.?P\.?C\.?|Code of Criminal Procedure|Indian Evidence Act)\b", re.I
)
SECTION_REF = re.compile(
    r"(?:\b(?:section|sec\.?|u/s\.?|s\.|article|art\.|rule|order)\s*|धारा\s*)(\d+[A-Z]?(?:\(\d+\))?)", re.I
)
CASE_LAW = re.compile(r"\b[A-Z][\w.&]+(?:\s+[A-Z][\w.&]+)*\s+(?:v\.|vs\.?|versus)\s+[A-Z][\w.&]+", re.U)
# Accepts [[KB:id]] and the sloppy variants weaker models produce: [KB:id], [[KB:a], [KB:b]]
TAG = re.compile(r"\[{1,2}\s*KB\s*:\s*([\w\-]+)\s*\]{1,2}", re.I)


@lru_cache(maxsize=1)
def load_kb() -> dict[str, dict]:
    data = json.loads(KB_PATH.read_text(encoding="utf-8"))
    return {e["id"]: e for e in data["entries"]}


def entries_for(problem_type: str | None) -> list[dict]:
    kb = load_kb()
    pt = problem_type or "other"
    hits = [e for e in kb.values() if pt in e["applies_to"]]
    if pt == "other":  # unknown yet: give the general entries + one from each area
        hits = [e for e in kb.values() if "other" in e["applies_to"] or e["id"] in ("legal-notice", "cpa-35", "cow-45", "rent-state-law")]
    return hits


def kb_prompt_block(entries: list[dict]) -> str:
    lines = []
    for e in entries:
        sec = f" s.{e['section']}" if e.get("section") else ""
        flag = "" if e["status"] == "verified" else " (needs verification)"
        lines.append(f"[[KB:{e['id']}]] {e['law']}{sec} - {e['title']}{flag}: {e['summary']}")
    return "\n".join(lines)


def cite_label(e: dict) -> str:
    sec = f", s. {e['section']}" if e.get("section") and not str(e["section"]).startswith(("Order", "Rule", "Schedule", "Fee")) else (f", {e['section']}" if e.get("section") else "")
    return f"{e['law']}{sec}"


def _known_numbers() -> set[str]:
    nums = set()
    for e in load_kb().values():
        for n in re.findall(r"\d+", str(e.get("section") or "")):
            nums.add(n)
    nums.update({"142"})  # referenced inside ni-138 summary
    return nums


def validate(text: str) -> dict:
    """Turn [[KB:id]] tags into numbered citations and flag anything unverifiable.

    Returns {"text": rendered markdown, "citations": [entry...], "warnings": [str...]}.
    """
    kb = load_kb()
    citations: list[dict] = []
    warnings: list[str] = []

    def repl(m):
        kid = m.group(1).lower()
        e = kb.get(kid)
        if not e:
            warnings.append(f"Removed a citation to an unknown source ('{kid}').")
            return ""
        if e not in citations:
            citations.append(e)
        return f" **[{citations.index(e) + 1}]**"

    rendered = TAG.sub(repl, text)

    # Check raw legal references the model wrote outside the tag system.
    known = _known_numbers()
    for sent in re.split(r"(?<=[.!?।\n])\s+", TAG.sub("", text)):
        if REPEALED.search(sent) and SECTION_REF.search(sent):
            warnings.append(
                f"Mentions a section of a repealed law (IPC/CrPC/Evidence Act were replaced on 1 July 2024): \"{sent.strip()[:140]}\""
            )
            continue
        for m in SECTION_REF.finditer(sent):
            num = re.match(r"\d+", m.group(1)).group(0)
            if num not in known:
                warnings.append(f"Unverified legal reference '{m.group(0).strip()}' - not in the verified knowledge base; confirm with a lawyer.")
        if CASE_LAW.search(sent):
            warnings.append(f"Mentions a court case that this app cannot verify: \"{CASE_LAW.search(sent).group(0)}\"")
    # dedupe, keep order
    seen, uniq = set(), []
    for w in warnings:
        if w not in seen:
            seen.add(w)
            uniq.append(w)
    return {"text": rendered.strip(), "citations": [e["id"] for e in citations], "warnings": uniq}
