"""UI-independent pipeline (used by the Streamlit app AND the eval runner).

One user turn:
  files -> vault ingest (AI index card)       [LLM, multimodal]
  conversation -> structured case facts       [LLM, JSON]
  facts -> forum / deadlines / referral       [CODE rules]
  facts + rules + verified KB -> reply        [LLM]
  reply -> citation validator                 [CODE]
"""
from __future__ import annotations

import io
import json
import re
from pathlib import Path
from datetime import date

from . import kb, rules, store, vault
from .llm import LLM
from .prompts import ASSISTANT, DRAFT, EXPLAIN_DOC, EXTRACT, PRACTICE, PRACTICE_FEEDBACK
from .vault import fill

WELCOME = (
    "Namaste! I'm **Nyaya**, an AI legal-help assistant (not a lawyer). Tell me what happened - in any language, "
    "as messy as you like. You can type, record your voice, or attach photos, screenshots, PDFs and recordings.\n\n"
    "I help most with: **security deposit not returned · salary not paid · refund/defective product · a notice you received**.\n\n"
    "_Aap Hindi ya Hinglish mein bhi likh/bol sakte hain._"
)


def files_brief(case: dict) -> str:
    if not case["files"]:
        return "(no files uploaded yet)"
    return "\n".join(vault.catalog_line(f)[:300] for f in case["files"])


def conversation_text(msgs: list[dict], n: int = 10) -> str:
    return "\n".join(f"{m['role'].upper()}: {m['content']}" for m in msgs[-n:])


def update_facts(case: dict, llm: LLM) -> None:
    prompt = fill(EXTRACT, facts=case["facts"], files=files_brief(case), conversation=conversation_text(case["messages"], 12))
    try:
        new = llm.chat_json([{"role": "user", "content": prompt}])
        base = store.empty_facts()
        base.update({k: v for k, v in new.items() if k in base})
        case["facts"] = base
    except Exception as e:  # noqa: BLE001 - keep old facts if extraction fails
        case.setdefault("errors", []).append(f"extract: {str(e)[:200]}")


def all_user_text(case: dict) -> str:
    return " ".join(m["content"] for m in case["messages"] if m["role"] == "user")


def process_turn(case: dict, llm: LLM, text: str, uploads: list[tuple[str, bytes]] | None = None,
                 audio: tuple[str, bytes] | None = None, base=None) -> dict:
    """Mutates and saves `case`; returns the assistant message dict."""
    parts = []
    if audio:
        try:
            transcript = llm.transcribe(audio[1], audio[0])
            parts.append(f"(voice) {transcript}")
        except Exception as e:  # noqa: BLE001
            parts.append(f"[voice note could not be transcribed: {str(e)[:100]}]")
            vault.ingest(case, None, audio[0], audio[1], note="voice message (untranscribed)", source="chat", base=base, analyze=False)
    if text:
        parts.append(text)
    user_msg = {"role": "user", "content": "\n".join(parts).strip(), "ts": store.now(), "file_ids": []}
    case["messages"].append(user_msg)

    for name, data in uploads or []:
        rec = vault.ingest(case, llm, name, data, note=text[:200] if text else "", source="chat", base=base)
        user_msg["file_ids"].append(rec["id"])
    if user_msg["file_ids"]:
        titles = [f"{f['id']}: {(f.get('ai') or {}).get('title') or f['filename']}" for f in case["files"] if f["id"] in user_msg["file_ids"]]
        user_msg["content"] += "\n[Uploaded to vault: " + "; ".join(titles) + "]"

    if case["title"] == "New case" and user_msg["content"]:
        case["title"] = re.sub(r"\s+", " ", user_msg["content"].replace("(voice)", ""))[:48].strip() or "New case"

    update_facts(case, llm)
    if not case.get("title_locked") and (case["facts"].get("case_title") or "").strip():
        case["title"] = case["facts"]["case_title"].strip()[:60]
    analysis = rules.analyze(case["facts"], all_user_text(case))

    entries = kb.entries_for(case["facts"].get("problem_type"))
    system = fill(
        ASSISTANT, today=date.today().isoformat(), kb=kb.kb_prompt_block(entries),
        language=case["facts"].get("language") or "the same language and script as the user's latest message",
        rules=json.dumps({k: analysis[k] for k in ("scope_note", "forum", "deadlines", "referral", "checklist")}, ensure_ascii=False),
        facts=case["facts"], missing="\n".join(f"- {q}" for q in case["facts"].get("missing_info") or []) or "- (none)",
        files=files_brief(case),
    )
    msgs = [{"role": "system", "content": system}] + [
        {"role": m["role"], "content": m["content"]} for m in case["messages"][-14:]
    ]
    try:
        raw = llm.chat(msgs, temperature=0.4)
    except Exception as e:  # noqa: BLE001
        raw = f"The AI model is unavailable right now ({str(e)[:160]}). Your message and files are saved - please try again."
    checked = kb.validate(raw)
    reply = {"role": "assistant", "content": checked["text"], "raw": raw, "citations": checked["citations"],
             "warnings": checked["warnings"], "referral": analysis["referral"], "ts": store.now(),
             "model": getattr(llm, "last_model", llm.model)}
    case["messages"].append(reply)
    case["analysis"] = analysis
    store.save(case, base)
    return reply


# ------------------------------------------------------------------ documents
DOC_TYPES = {
    "Legal notice / demand notice": "legal notice demanding the money/refund owed",
    "Consumer complaint (District Commission)": "consumer complaint to be filed before the District Consumer Disputes Redressal Commission (format: parties, facts, deficiency, cause of action, jurisdiction, limitation, relief claimed, verification)",
    "Grievance email to company / e-commerce grievance officer": "short firm grievance email to the company's grievance officer / customer care",
    "Complaint to Labour Department (unpaid wages)": "written complaint/application to the Labour Commissioner/wage authority for unpaid wages",
    "Reply to a notice I received": "reply to the notice the user received, stating the user's side point by point without admitting liability",
    "Written complaint to Police (only for threats/cheating)": "written complaint to the Station House Officer describing incidents factually (only use if the case involves threats, abuse or cheating; note that pure money disputes are usually civil)",
    "Case summary for a lawyer / DLSA": "one-page case brief for a lawyer or District Legal Services Authority: parties, timeline, amounts, evidence list, questions to ask the lawyer",
}


def draft_document(case: dict, llm: LLM, doc_type: str, language: str = "English", extra: str = "") -> dict:
    analysis = rules.analyze(case["facts"], all_user_text(case))
    entries = kb.entries_for(case["facts"].get("problem_type"))
    prompt = fill(DRAFT, doc_type=DOC_TYPES.get(doc_type, doc_type), today=date.today().strftime("%d %B %Y"), language=language,
                  extra=f"- Extra instructions from the user: {extra}" if extra else "", kb=kb.kb_prompt_block(entries),
                  rules=json.dumps({k: analysis[k] for k in ("forum", "deadlines")}, ensure_ascii=False),
                  facts=case["facts"], files=files_brief(case))
    raw = llm.chat([{"role": "user", "content": prompt}], temperature=0.2)
    checked = kb.validate(raw)
    text = checked["text"]
    if checked["citations"]:
        text += "\n\nReferences:\n" + "\n".join(
            f"[{i + 1}] {kb.cite_label(kb.load_kb()[c])} - {kb.load_kb()[c]['title']}" for i, c in enumerate(checked["citations"]))
    doc = {"id": f"D{len(case['documents']) + 1}", "type": doc_type, "language": language, "created": store.now(),
           "content": text, "warnings": checked["warnings"], "placeholders": re.findall(r"\[FILL:[^\]]+\]", text)}
    case["documents"].append(doc)
    store.save(case)
    return doc


def to_docx(title: str, text: str) -> bytes:
    import docx
    from docx.shared import Pt
    d = docx.Document()
    style = d.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    d.add_heading(title, level=1)
    for line in text.split("\n"):
        line = line.replace("**", "")
        if line.strip().startswith("#"):
            d.add_heading(line.strip("# ").strip(), level=2)
        else:
            d.add_paragraph(line)
    buf = io.BytesIO()
    d.save(buf)
    return buf.getvalue()


def split_doc(text: str) -> tuple[str, str]:
    """Separate the sendable document (+ its References) from the private 'NOTES FOR YOU' advice."""
    m = re.search(r"\n\s*-{3,}\s*\n\s*\**\s*NOTES FOR YOU:?\s*\**", text, re.I)
    if not m:
        return text.strip(), ""
    doc, rest = text[:m.start()], text[m.end():]
    ri = rest.find("\nReferences:")
    notes = rest[:ri] if ri != -1 else rest
    if ri != -1:
        doc += "\n\n" + rest[ri:].strip()
    return doc.strip(), notes.strip()


FONT_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"
DEVANAGARI = re.compile(r"[ऀ-ॿ]")


def to_pdf(title: str, text: str) -> bytes:
    """Print-ready A4 PDF. Bundled Noto fonts + HarfBuzz shaping so Hindi (Devanagari) renders correctly."""
    from fpdf import FPDF

    pdf = FPDF(format="A4")
    pdf.set_margins(20, 18, 20)
    pdf.set_auto_page_break(True, 18)
    pdf.add_font("Noto", "", str(FONT_DIR / "NotoSans-Regular.ttf"))
    pdf.add_font("Noto", "B", str(FONT_DIR / "NotoSans-Bold.ttf"))
    pdf.add_font("Deva", "", str(FONT_DIR / "NotoSansDevanagari-Regular.ttf"))
    pdf.add_font("Deva", "B", str(FONT_DIR / "NotoSansDevanagari-Bold.ttf"))
    hindi = bool(DEVANAGARI.search(text))
    main, other = ("Deva", "Noto") if hindi else ("Noto", "Deva")
    pdf.set_fallback_fonts([other])
    pdf.set_text_shaping(True)
    pdf.add_page()
    pdf.set_font(main, "B", 14)
    pdf.multi_cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    for line in text.split("\n"):
        raw = line.strip()
        if not raw:
            pdf.ln(3)
            continue
        bold = raw.startswith("#") or (raw.startswith("**") and raw.endswith("**"))
        clean = raw.lstrip("#").strip().replace("**", "")
        if raw == "---":
            pdf.ln(2)
            pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
            pdf.ln(3)
            continue
        pdf.set_font(main, "B" if bold else "", 11 if bold else 10.5)
        pdf.multi_cell(0, 5.8, clean, new_x="LMARGIN", new_y="NEXT")
    return bytes(pdf.output())


def case_summary_md(case: dict, analysis: dict) -> str:
    """Deterministic case-file export (no LLM): what a lawyer / DLSA / police desk needs at a glance."""
    f = case["facts"]
    L = [f"Problem: {rules.SCOPE.get(f.get('problem_type'), f.get('problem_type') or '-')}", f"Summary: {f.get('summary') or '-'}",
         f"Location: {', '.join(x for x in [(f.get('location') or {}).get('city'), (f.get('location') or {}).get('state')] if x) or '-'}",
         f"Amount in dispute: {f.get('amount_in_dispute_inr') or '-'}", "", "## People involved"]
    L += [f"- {p.get('name') or '?'} - {p.get('role') or '?'} - phone: {p.get('phone') or '-'} - address: {p.get('address') or '-'}" for p in f.get("parties", [])] or ["- none recorded"]
    L += ["", "## Timeline"] + ([f"- {t.get('date')}: {t.get('event')}" for t in f.get("timeline", [])] or ["- none"])
    L += ["", "## Evidence"] + ([f"- [{e.get('status')}] {e.get('item')} {('(vault ' + ', '.join(e.get('file_ids') or []) + ')') if e.get('file_ids') else ''}" for e in f.get("evidence", [])] or ["- none"])
    L += ["", "## Vault files"] + [f"- {x['id']}: {(x.get('ai') or {}).get('title') or x['filename']}" for x in case["files"]]
    L += ["", "## Forum & deadlines (rule-based, verify with a lawyer)"]
    L += [f"- {fo['forum']}" for fo in analysis.get("forum", [])]
    L += [f"- {d['label']}: {d.get('last_date') or d.get('note')}" for d in analysis.get("deadlines", [])]
    L += ["", "## Open questions"] + [f"- {q}" for q in f.get("missing_info") or []]
    L += ["", "Prepared with Nyaya (AI legal-help assistant, not a lawyer). Free legal aid: NALSA 15100."]
    return "\n".join(L)


# ------------------------------------------------------------------ practice
def other_side_role(case: dict) -> str:
    pt = case["facts"].get("problem_type")
    for p in case["facts"].get("parties", []):
        if p.get("role"):
            return f"{p.get('name') or 'the other party'} ({p['role']})"
    return {"deposit": "the landlord", "salary": "the employer's HR manager", "consumer": "the company's customer-care manager"}.get(pt, "the other party")


def practice_reply(case: dict, llm: LLM, user_text: str) -> str:
    pr = case["practice"]
    pr["messages"].append({"role": "user", "content": user_text})
    sys = fill(PRACTICE, role=other_side_role(case), summary=case["facts"].get("summary") or "(see conversation)",
               language=case["facts"].get("language") or "the user's language")
    reply = llm.chat([{"role": "system", "content": sys}] + pr["messages"][-16:], temperature=0.7)
    pr["messages"].append({"role": "assistant", "content": reply})
    store.save(case)
    return reply


def practice_feedback(case: dict, llm: LLM) -> dict:
    pr = case["practice"]
    transcript = "\n".join(f"{'USER' if m['role'] == 'user' else 'OTHER SIDE'}: {m['content']}" for m in pr["messages"])
    evidence = ", ".join(e.get("item", "") for e in case["facts"].get("evidence", []) if e.get("status") == "uploaded") or "none uploaded"
    prompt = fill(PRACTICE_FEEDBACK, role=other_side_role(case), summary=case["facts"].get("summary") or "", evidence=evidence,
                  transcript=transcript, language=case["facts"].get("language") or "English",
                  kb=kb.kb_prompt_block(kb.entries_for(case["facts"].get("problem_type"))))
    checked = kb.validate(llm.chat([{"role": "user", "content": prompt}], temperature=0.3))
    pr["feedback"] = checked
    store.save(case)
    return checked


# ------------------------------------------------------------------ explain a document
def explain_file(case: dict, llm: LLM, f: dict, language: str | None = None) -> dict:
    language = language or case["facts"].get("language") or "English"
    entries = kb.entries_for("notice_received") + kb.entries_for(case["facts"].get("problem_type"))
    entries = list({e["id"]: e for e in entries}.values())
    if f["kind"] == "image":
        data = store.file_path(case, f).read_bytes()
        content = "(see attached image)"
        prompt = fill(EXPLAIN_DOC, language=language, kb=kb.kb_prompt_block(entries), content=content)
        import base64
        msgs = [{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:{f['mime']};base64,{base64.b64encode(data).decode()}"}}]}]
        raw = llm._complete(msgs, model=llm.vision_model, temperature=0.2)
    else:
        content = f.get("text") or f.get("transcript") or (f.get("ai") or {}).get("key_text") or ""
        raw = llm.chat([{"role": "user", "content": fill(EXPLAIN_DOC, language=language, kb=kb.kb_prompt_block(entries), content=content[:12000])}], temperature=0.2)
    out = kb.validate(raw)
    f["explanation"] = out
    store.save(case)
    return out
