"""Evidence vault: ingest any file -> AI index card; find files from vague (spoken) requests.

Retrieval is two-stage:
 1. instant lexical match (code; synonym expansion + party-alias resolution) - works offline, no API cost
 2. LLM re-rank over the whole case catalog (resolves "the guy from the office" -> HR manager Rohit)
If the LLM is unavailable, stage 1 results are still shown.
"""
from __future__ import annotations

import io
import json
import mimetypes
import re

from . import store
from .llm import LLM
from .prompts import FILE_ANALYZE, SEARCH


def fill(template: str, **kw) -> str:
    t = template.replace("{{", "{").replace("}}", "}")
    for k, v in kw.items():
        t = t.replace("{" + k + "}", v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, indent=1))
    return t


IMAGE_EXT = {"png", "jpg", "jpeg", "webp", "gif", "bmp"}
AUDIO_EXT = {"wav", "mp3", "m4a", "ogg", "aac", "webm", "flac"}


def kind_of(filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext in IMAGE_EXT:
        return "image"
    if ext in AUDIO_EXT:
        return "audio"
    if ext == "pdf":
        return "pdf"
    if ext in ("docx",):
        return "docx"
    if ext in ("txt", "md", "csv", "json", "eml"):
        return "text"
    return "other"


def extract_text(kind: str, data: bytes) -> str:
    try:
        if kind == "pdf":
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(data))
            return "\n".join((p.extract_text() or "") for p in reader.pages[:15]).strip()
        if kind == "docx":
            import docx
            d = docx.Document(io.BytesIO(data))
            return "\n".join(p.text for p in d.paragraphs).strip()
        if kind == "text":
            return data.decode("utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001
        return f"[could not read text: {e}]"
    return ""


def case_context(case: dict) -> str:
    f = case["facts"]
    parties = "; ".join(
        f"{p.get('name') or '?'} ({p.get('role') or '?'}; aka {', '.join(p.get('aliases') or []) or '-'})" for p in f.get("parties", [])
    )
    recent = " | ".join(m["content"][:200] for m in case["messages"][-6:] if m["role"] == "user")
    return f"Problem: {f.get('problem_type')}. Summary: {f.get('summary') or '-'}. Parties: {parties or '-'}. Recent user messages: {recent or '-'}"


def ingest(case: dict, llm: LLM | None, filename: str, data: bytes, note: str = "", source: str = "vault",
           base=None, analyze: bool = True) -> dict:
    fid = store.next_file_id(case)
    safe = re.sub(r"[^\w.\-]+", "_", filename)[-80:]
    kind = kind_of(filename)
    rec = {
        "id": fid, "filename": filename, "stored_name": f"{fid}_{safe}", "kind": kind,
        "mime": mimetypes.guess_type(filename)[0] or "application/octet-stream",
        "size": len(data), "uploaded_at": store.now(), "source": source, "user_note": note,
        "transcript": None, "text": None, "ai": None, "ai_error": None,
    }
    store.file_path(case, rec, base).write_bytes(data)
    case["files"].append(rec)
    if analyze and llm is not None:
        analyze_file(case, rec, data, llm)
    store.save(case, base)
    return rec


def analyze_file(case: dict, rec: dict, data: bytes, llm: LLM) -> None:
    kind = rec["kind"]
    ctx = case_context(case)
    try:
        if kind == "image":
            prompt = fill(FILE_ANALYZE, context=ctx, note=rec["user_note"] or "-", filename=rec["filename"],
                          content_hint="The image is attached. Read ALL visible text (OCR), including chat bubbles, names, timestamps.")
            rec["ai"] = llm.image_json(prompt, data, rec["mime"])
        else:
            if kind == "audio":
                rec["transcript"] = llm.transcribe(data, rec["filename"])
                body = f"AUDIO TRANSCRIPT:\n{rec['transcript'][:6000]}"
            elif kind in ("pdf", "docx", "text"):
                rec["text"] = extract_text(kind, data)[:20000]
                body = f"DOCUMENT TEXT:\n{rec['text'][:8000] or '[no extractable text - maybe a scanned PDF]'}"
            else:
                body = "[binary file - no content available; rely on file name and note]"
            prompt = fill(FILE_ANALYZE, context=ctx, note=rec["user_note"] or "-", filename=rec["filename"], content_hint=body)
            rec["ai"] = llm.chat_json([{"role": "user", "content": prompt}])
    except Exception as e:  # noqa: BLE001 - keep the file even if AI indexing fails
        rec["ai_error"] = str(e)[:300]


def add_note(case: dict, title: str, text: str, base=None) -> dict:
    """A typed note (e.g. landlord's phone number) is also a vault item."""
    rec = ingest(case, None, f"{re.sub(r'[^A-Za-z0-9]+', '_', title)[:40] or 'note'}.txt", text.encode("utf-8"),
                 note=title, source="note", base=base, analyze=False)
    rec["text"] = text
    rec["ai"] = {"title": title, "category": "note", "description": text[:300], "people": [], "dates": [], "amounts": [],
                 "key_text": text[:400], "tags": _tokens(title + " " + text)[:15], "relevance": ""}
    store.save(case, base)
    return rec


# ---------------------------------------------------------------- retrieval
SYNONYMS = {
    "screenshot": ["chat", "image", "whatsapp", "message", "screen", "chat_screenshot"],
    "chat": ["whatsapp", "message", "screenshot", "sms", "chat_screenshot"],
    "whatsapp": ["chat", "message", "screenshot"],
    "audio": ["recording", "voice", "call", "audio_recording"],
    "recording": ["audio", "voice", "call", "audio_recording"],
    "call": ["audio", "recording", "phone"],
    "voice": ["audio", "recording"],
    "lease": ["agreement", "rent", "rental", "tenancy", "licence", "agreement_contract"],
    "agreement": ["lease", "contract", "rent", "agreement_contract"],
    "contract": ["agreement", "lease", "offer", "appointment"],
    "salary": ["wages", "pay", "payment", "salary_slip", "payslip"],
    "pay": ["salary", "payment", "wages"],
    "receipt": ["invoice", "bill", "payment", "receipt_invoice", "payment_proof"],
    "invoice": ["bill", "receipt", "order", "receipt_invoice"],
    "bill": ["invoice", "receipt"],
    "proof": ["payment_proof", "receipt", "transfer", "upi"],
    "paid": ["payment", "payment_proof", "upi", "transfer"],
    "deposit": ["security", "advance", "payment"],
    "photo": ["image", "picture", "pic", "photo_of_person", "photo_of_property_or_item"],
    "picture": ["photo", "image"],
    "pic": ["photo", "image"],
    "face": ["photo_of_person", "photo", "person"],
    "id": ["id_document", "aadhaar", "card", "identity"],
    "number": ["phone", "mobile", "contact"],
    "phone": ["number", "mobile", "contact"],
    "notice": ["letter", "notice_or_letter", "legal"],
    "letter": ["notice", "notice_or_letter"],
    "office": ["hr", "manager", "boss", "employer", "company", "work"],
    "boss": ["manager", "hr", "employer", "office"],
    "landlord": ["owner", "house", "flat", "rent"],
    "owner": ["landlord"],
    "abuse": ["abusive", "fuck", "insult", "threat", "rude", "gaali"],
    "fuck": ["abuse", "abusive", "insult"],
    "slip": ["salary_slip", "payslip"],
    "bank": ["statement", "bank_statement", "transfer"],
}
STOP = set("""a an the of to for me my i is was he she it his her their them they this that these those and or but with from in on at by
give show find get pull want need please uh um like what who which when where how do did does have has had be been just one
mean the- him guy file thing something remember dont don't know name""".split())


def _tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9ऀ-ॿ]+", (text or "").lower()) if t not in STOP and len(t) > 1]


def _haystack(f: dict) -> str:
    ai = f.get("ai") or {}
    people = " ".join(f"{p.get('name') or ''} {p.get('role') or ''} {p.get('matches_party') or ''}" for p in ai.get("people", []) if isinstance(p, dict))
    return " ".join(str(x) for x in [
        f["filename"], f.get("user_note"), f["kind"], ai.get("title"), ai.get("category"), ai.get("description"),
        people, ai.get("key_text"), " ".join(ai.get("tags") or []), " ".join(map(str, ai.get("dates") or [])),
        (f.get("transcript") or "")[:1500], (f.get("text") or "")[:1500],
    ] if x)


def _expand(query: str, case: dict) -> dict[str, float]:
    weights: dict[str, float] = {}
    toks = _tokens(query)
    for t in toks:
        weights[t] = max(weights.get(t, 0), 1.0)
        for s in SYNONYMS.get(t, []):
            weights[s] = max(weights.get(s, 0), 0.6)
    # party alias resolution: "the office guy" -> add that party's name and role
    qlow = query.lower()
    for p in case["facts"].get("parties", []):
        labels = [p.get("name") or "", p.get("role") or "", *(p.get("aliases") or [])]
        if any(lbl and (lbl.lower() in qlow or set(_tokens(lbl)) & set(toks)) for lbl in labels):
            for t in _tokens(" ".join(labels)):
                weights[t] = max(weights.get(t, 0), 0.8)
    return weights


def lexical_search(query: str, cases: list[dict], k: int = 6) -> list[dict]:
    results = []
    for case in cases:
        w = _expand(query, case)
        if not w:
            continue
        for f in case["files"]:
            hay = set(_tokens(_haystack(f)))
            score = sum(v for t, v in w.items() if t in hay)
            if score > 0:
                results.append({"case_id": case["id"], "case_title": case["title"], "file": f,
                                "score": round(score / (sum(w.values()) ** 0.5), 3), "reason": "keyword match"})
    return sorted(results, key=lambda r: -r["score"])[:k]


def catalog_line(f: dict) -> str:
    ai = f.get("ai") or {}
    people = ", ".join(f"{p.get('name') or '?'} ({p.get('role') or '?'})" for p in ai.get("people", []) if isinstance(p, dict))
    return (f"{f['id']} | {f['kind']}/{ai.get('category', '?')} | {ai.get('title') or f['filename']} | "
            f"people: {people or '-'} | dates: {', '.join(map(str, ai.get('dates') or [])) or '-'} | "
            f"note: {f.get('user_note') or '-'} | {(ai.get('description') or '')[:200]} | text: {(ai.get('key_text') or f.get('transcript') or f.get('text') or '')[:200]}")


def smart_search(query: str, case: dict, llm: LLM | None) -> dict:
    """LLM re-rank for one case. Falls back to lexical on any failure."""
    lex = lexical_search(query, [case])
    if not case["files"]:
        return {"interpretation": "Vault is empty.", "results": [], "mode": "none"}
    if llm is None or not llm.configured:
        return {"interpretation": "(AI unavailable - keyword matches)", "results": lex, "mode": "lexical"}
    parties = "\n".join(
        f"- {p.get('name') or '?'}: {p.get('role') or '?'}; aliases: {', '.join(p.get('aliases') or []) or '-'}; {p.get('description') or ''}"
        for p in case["facts"].get("parties", [])) or "- (none recorded)"
    prompt = fill(SEARCH, parties=parties, catalog="\n".join(catalog_line(f) for f in case["files"]), query=query)
    try:
        out = llm.chat_json([{"role": "user", "content": prompt}])
        by_id = {f["id"]: f for f in case["files"]}
        res = []
        for m in out.get("matches", []):
            f = by_id.get(str(m.get("id")))
            if f:
                res.append({"case_id": case["id"], "case_title": case["title"], "file": f,
                            "score": float(m.get("confidence") or 0), "reason": m.get("reason", "")})
        return {"interpretation": out.get("interpretation", ""), "results": res, "mode": "ai"}
    except Exception as e:  # noqa: BLE001
        return {"interpretation": f"(AI search failed: {str(e)[:120]} - showing keyword matches)", "results": lex, "mode": "lexical"}
