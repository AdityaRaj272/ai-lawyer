"""Nyaya - AI legal help for everyday problems in India (Streamlit UI)."""
from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()
try:  # Streamlit Cloud secrets -> env
    for _k, _v in st.secrets.items():
        if isinstance(_v, (str, int, float, bool)):  # skip sections like [auth]
            os.environ.setdefault(_k, str(_v))
except Exception:  # noqa: BLE001
    pass

from core import engine, kb, rules, store, vault  # noqa: E402
from core.llm import LLM, PRESETS, LLMError  # noqa: E402

st.set_page_config(page_title="Nyaya - AI legal help", page_icon=":material/balance:", layout="wide")

# Hamburger icon on both sidebar toggles (Streamlit draws a double-arrow by default) and keep the
# collapse control visible instead of hover-only.
st.markdown("""
<style>
[data-testid="stSidebarCollapseButton"] { visibility: visible !important; }
[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
[data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"] { font-size: 0 !important; }
[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"]::before,
[data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"]::before {
  content: "menu"; font-family: "Material Symbols Rounded"; font-size: 1.6rem; line-height: 1;
  font-feature-settings: "liga"; -webkit-font-feature-settings: "liga";
}
/* only the case-title buttons (keys open_<id>): left-aligned, one line, ellipsis */
.st-key-case_list [class*="st-key-open_"] button { justify-content: flex-start; min-height: 2.1rem; }
.st-key-case_list [class*="st-key-open_"] button div,
.st-key-case_list [class*="st-key-open_"] button p {
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; text-align: left; max-width: 100%;
}
/* the ... menu button: just the icon, no dropdown chevron */
.st-key-case_list [data-testid="stPopover"] button { padding-left: 0.4rem; padding-right: 0.4rem; justify-content: center; }
.st-key-case_list [data-testid="stPopover"] button [data-testid="stIconMaterial"] + div:empty { display: none; }
</style>
""", unsafe_allow_html=True)

def auth_configured() -> bool:
    """Google sign-in is on only when .streamlit/secrets.toml has a complete [auth] section."""
    try:
        a = st.secrets.get("auth", {})
        return all(a.get(k) for k in ("redirect_uri", "cookie_secret", "client_id", "client_secret", "server_metadata_url"))
    except Exception:  # noqa: BLE001 - no secrets file at all
        return False


AUTH = auth_configured()
if AUTH and not st.user.get("is_logged_in", False):
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.title(":material/balance: Nyaya")
        st.markdown("AI legal help for everyday problems in India - security deposits, unpaid salary, refunds and notices. "
                    "Your cases and evidence are private to your account.")
        st.button("Sign in with Google", icon=":material/login:", type="primary", on_click=st.login, width="stretch")
        st.caption("Nyaya is an AI assistant, not a lawyer. Free legal aid: NALSA 15100.")
    st.stop()
USER_ID = st.user.email if AUTH else None
ROOT = store.user_root(USER_ID)

I = {  # one place for every icon (Material Symbols)
    "app": ":material/balance:", "user": ":material/person:", "other_side": ":material/record_voice_over:",
    "talk": ":material/forum:", "case": ":material/folder_open:", "vault": ":material/inventory_2:",
    "docs": ":material/description:", "practice": ":material/sports_kabaddi:", "model": ":material/memory:",
    "ok": ":material/check_circle:", "key": ":material/key:", "add": ":material/add:", "delete": ":material/delete:",
    "lawyer": ":material/gavel:", "sources": ":material/menu_book:", "warn": ":material/report:",
    "download": ":material/download:", "save": ":material/save:", "search": ":material/search:",
    "mic": ":material/mic:", "upload": ":material/upload_file:", "note": ":material/sticky_note_2:",
    "people": ":material/group:", "timeline": ":material/schedule:", "evidence": ":material/fact_check:",
    "stand": ":material/explore:", "question": ":material/help:", "phone": ":material/call:",
    "explain": ":material/plagiarism:", "retry": ":material/refresh:", "draft": ":material/edit_document:",
    "feedback": ":material/rate_review:", "restart": ":material/restart_alt:", "tag": ":material/sell:",
    "best": ":material/star:", "file": ":material/attach_file:", "deadline": ":material/event:",
    "pending": ":material/hourglass_empty:",
}
CAT_ICON = {"chat_screenshot": ":material/chat:", "agreement_contract": ":material/history_edu:",
            "payment_proof": ":material/payments:", "receipt_invoice": ":material/receipt_long:",
            "photo_of_person": ":material/person:", "id_document": ":material/badge:",
            "photo_of_property_or_item": ":material/photo_camera:", "audio_recording": ":material/mic:",
            "notice_or_letter": ":material/mail:", "email": ":material/alternate_email:",
            "salary_slip": ":material/request_quote:", "bank_statement": ":material/account_balance:",
            "note": ":material/sticky_note_2:", "generated_document": ":material/description:", "other": ":material/attach_file:"}
UPLOAD_TYPES = ["png", "jpg", "jpeg", "webp", "pdf", "txt", "docx", "mp3", "wav", "m4a", "ogg", "webm"]

# ------------------------------------------------------------------ sidebar: model + cases
with st.sidebar:
    st.title(f"{I['app']} Nyaya")
    st.caption("AI legal help for everyday problems in India. Not a lawyer.")
    if AUTH:
        u1, u2 = st.columns([4, 1], vertical_alignment="center")
        u1.caption(f":material/account_circle: {st.user.get('name') or USER_ID}")
        u2.button("", icon=":material/logout:", help="Sign out", on_click=st.logout, key="logout")
    else:
        st.caption(":material/person_off: Guest mode - cases are stored on this computer only")

    # ---- cases, listed like chats ----
    cases = store.list_cases(ROOT)
    if "case_id" not in st.session_state or not any(c["id"] == st.session_state.case_id for c in cases):
        st.session_state.case_id = cases[0]["id"] if cases else store.new_case(base=ROOT)["id"]
        cases = store.list_cases(ROOT)
    if st.button("New case", icon=I["add"], width="stretch", key="new_case"):
        empty = next((c for c in cases if not c["n_msgs"] and not c["n_files"]), None)  # reuse a blank case
        st.session_state.case_id = empty["id"] if empty else store.new_case(base=ROOT)["id"]
        st.rerun()
    st.caption("Your cases")
    with st.container(key="case_list"):
        for c in cases:
            active = c["id"] == st.session_state.case_id
            row, menu = st.columns([5, 1], vertical_alignment="center", gap="medium")
            if row.button(c["title"], key=f"open_{c['id']}", type="secondary" if active else "tertiary", width="stretch",
                          help=c["title"] if len(c["title"]) > 28 else None):
                st.session_state.case_id = c["id"]
                st.rerun()
            with menu.popover("", icon=":material/more_horiz:", help="Rename or delete"):
                new_title = st.text_input("Case name", value=c["title"], key=f"rn_{c['id']}")
                if st.button("Rename", icon=":material/edit:", key=f"rns_{c['id']}", width="stretch"):
                    _c = store.load(c["id"], ROOT)
                    _c["title"], _c["title_locked"] = new_title.strip()[:60] or _c["title"], True
                    store.save(_c)
                    st.rerun()
                if st.button("Delete case", icon=I["delete"], key=f"del_{c['id']}", type="primary", width="stretch"):
                    store.delete_case(c["id"], ROOT)
                    if active:
                        st.session_state.pop("case_id")
                    st.rerun()
                st.caption(f"{c['n_files']} files · updated {c['updated'][:16].replace('T', ' ')}")

    st.divider()
    with st.expander("Model (swappable)", icon=I["model"], expanded=False):
        providers = list(PRESETS)
        default_p = os.getenv("LLM_PROVIDER", "gemini")
        provider = st.selectbox("Provider", providers, index=providers.index(default_p) if default_p in providers else 0)
        model = st.text_input("Model", value=os.getenv("LLM_MODEL") if provider == default_p and os.getenv("LLM_MODEL") else (PRESETS[provider]["model"] or ""))
        key_env = PRESETS[provider]["key_env"]
        if not os.getenv(key_env):
            k = st.text_input(f"{key_env}", type="password", help="Only kept in this server process' memory.")
            if k:
                os.environ[key_env] = k
    try:
        llm = LLM.from_env(provider, model or None)
    except LLMError as e:
        llm = None
        st.error(str(e), icon=I["warn"])
    if llm and llm.configured:
        st.caption(f"{I['ok']} Model: {llm.provider} / {llm.model}")
    else:
        st.error(f"Add {key_env} to .env (or above) to enable AI.", icon=I["key"])

    st.divider()
    st.caption("Covers in depth: security deposit · unpaid salary · consumer refunds · notices received. "
               "Free legal aid: **NALSA 15100** · Consumer helpline **1915** · Emergency **112**.")

case = store.load(st.session_state.case_id, ROOT)
analysis = case.get("analysis") or rules.analyze(case["facts"], engine.all_user_text(case))


def need_llm() -> bool:
    if not llm or not llm.configured:
        st.error("AI model not configured - add an API key in the sidebar.", icon=I["key"])
        return False
    return True


def render_citations(ids: list[str]):
    if not ids:
        return
    with st.expander(f"Sources ({len(ids)} verified)", icon=I["sources"]):
        k = kb.load_kb()
        for i, cid in enumerate(ids):
            e = k[cid]
            checks = " ".join(f"[{j + 1}]({u.split(' ')[0]})" for j, u in enumerate(e.get("verified_by") or []))
            st.markdown(f"**[{i + 1}] {kb.cite_label(e)}** - {e['title']}  \n{e['summary']}  \n"
                        f"<small>verified · [official text]({e['source']})" + (f" · checked against: {checks}" if checks else "") + "</small>",
                        unsafe_allow_html=True)


def render_warnings(ws: list[str]):
    for w in ws or []:
        st.caption(f"{I['warn']} {w}")


def render_file(c: dict, f: dict, ctx: str, big: bool = False):
    """ctx makes widget keys unique when the same file is shown in several places on one page."""
    p = store.file_path(c, f)
    if not p.exists():
        st.caption("(file missing on disk)")
        return
    data = p.read_bytes()
    if f["kind"] == "image":
        st.image(data, width="stretch" if big else 260)
    elif f["kind"] == "audio":
        st.audio(data)
        if f.get("transcript"):
            st.markdown(f"> {f['transcript'][:1500]}")
    elif f.get("text"):
        st.text(f["text"][:3000 if big else 600])
    st.download_button("Download original", data, file_name=f["filename"], icon=I["download"],
                       key=f"dl_{ctx}_{c['id']}_{f['id']}")


def file_label(f: dict) -> str:
    ai = f.get("ai") or {}
    return f"{CAT_ICON.get(ai.get('category'), I['file'])} {f['id']} · {ai.get('title') or f['filename']}"


# ------------------------------------------------------------------ header
st.subheader(case["title"])
ref = analysis.get("referral", {})
if ref.get("level") == "required":
    st.error("**You should talk to a real lawyer for this.** " + " ".join(ref["reasons"]) +
             " Free legal aid: call **15100** (NALSA) or visit your District Legal Services Authority.", icon=I["lawyer"])
elif ref.get("level") == "suggested":
    st.info("**Consider a lawyer's opinion.** " + " ".join(ref["reasons"]) + " Free help: NALSA **15100**.", icon=I["lawyer"])

tab_talk, tab_case, tab_vault, tab_docs, tab_practice = st.tabs(
    [f"{I['talk']} Talk", f"{I['case']} Case file", f"{I['vault']} Evidence vault", f"{I['docs']} Documents", f"{I['practice']} Practice"])

# ------------------------------------------------------------------ TALK
with tab_talk:
    with st.chat_message("assistant", avatar=I["app"]):
        st.markdown(engine.WELCOME)
    for m in case["messages"]:
        with st.chat_message(m["role"], avatar=I["app"] if m["role"] == "assistant" else I["user"]):
            st.markdown(m["content"])
            if m["role"] == "user" and m.get("file_ids"):
                imgs = [f for f in case["files"] if f["id"] in m["file_ids"] and f["kind"] == "image"]
                if imgs:
                    cols = st.columns(min(len(imgs), 4))
                    for col, f in zip(cols, imgs):
                        col.image(store.file_path(case, f).read_bytes(), width=140)
            if m["role"] == "assistant":
                render_citations(m.get("citations"))
                render_warnings(m.get("warnings"))

    val = st.chat_input("Describe your problem, attach proof, or record your voice", accept_file="multiple",
                        accept_audio=True, file_type=UPLOAD_TYPES, key="talk_input")
    if val and need_llm():
        text = val.text if hasattr(val, "text") else str(val)
        files = [(f.name, f.getvalue()) for f in (getattr(val, "files", None) or [])]
        audio = getattr(val, "audio", None)
        audio_t = ("voice.wav", audio.getvalue()) if audio else None
        with st.spinner("Reading your message and updating your case file..."):
            engine.process_turn(case, llm, text or "", files, audio_t)
        st.rerun()

# ------------------------------------------------------------------ CASE FILE
with tab_case:
    f = case["facts"]
    left, right = st.columns([3, 2])
    with left:
        st.markdown(f"**Problem type:** {rules.SCOPE.get(f.get('problem_type'), f.get('problem_type') or 'not clear yet')}")
        st.markdown(f"**Summary:** {f.get('summary') or '_Tell Nyaya what happened in the Talk tab._'}")
        loc = f.get("location") or {}
        st.markdown(f"**Where:** {', '.join(x for x in [loc.get('city'), loc.get('state')] if x) or '—'}  ·  "
                    f"**Amount in dispute:** {('Rs ' + format(int(f['amount_in_dispute_inr']), ',')) if f.get('amount_in_dispute_inr') else '—'}  ·  "
                    f"**Goal:** {f.get('user_goal') or '—'}")
        st.markdown(f"##### {I['people']} People involved")
        if f.get("parties"):
            st.dataframe([{"Name": p.get("name"), "Role": p.get("role"), "Phone": p.get("phone"), "Address": p.get("address"),
                           "Also called": ", ".join(p.get("aliases") or [])} for p in f["parties"]], hide_index=True, width="stretch")
        else:
            st.caption("None recorded yet.")
        st.markdown(f"##### {I['timeline']} Timeline")
        if f.get("timeline"):
            st.dataframe([{"Date": t.get("date"), "What happened": t.get("event"), "Source": t.get("source")} for t in f["timeline"]],
                         hide_index=True, width="stretch")
        else:
            st.caption("No events yet.")
        st.markdown(f"##### {I['evidence']} Evidence")
        status = {"uploaded": "In vault", "mentioned": "You have it - upload it", "needed": "Needed"}
        if f.get("evidence"):
            st.dataframe([{"Item": e.get("item"), "Status": status.get(e.get("status"), e.get("status")),
                           "Vault files": ", ".join(e.get("file_ids") or [])} for e in f["evidence"]], hide_index=True, width="stretch")
        with st.expander("Standard checklist for this problem type"):
            for item in analysis.get("checklist") or ["Describe your problem first."]:
                st.markdown(f"- {item}")
    with right:
        st.markdown(f"##### {I['stand']} Where you stand")
        st.caption("Computed by fixed rules, not guessed by the AI.")
        for fo in analysis.get("forum", []):
            e = kb.load_kb().get(fo.get("basis"))
            st.markdown(f"- **{fo['forum']}**" + (f"  \n  <small>basis: {kb.cite_label(e)}</small>" if e else "") +
                        (f"  \n  {fo['fee']}" if fo.get("fee") else ""), unsafe_allow_html=True)
        for d in analysis.get("deadlines", []):
            e = kb.load_kb().get(d.get("basis"))
            if d.get("last_date"):
                days = d["days_left"]
                left_txt = f":red[**{days} days left**]" if days < 30 else f"{days} days left"
                st.markdown(f"{I['deadline']} **{d['label']}:** by **{d['last_date']}** ({left_txt})  \n"
                            f"<small>counted from {d.get('counted_from')} · {kb.cite_label(e) if e else ''} · verify with a lawyer</small>", unsafe_allow_html=True)
            else:
                st.markdown(f"{I['pending']} **{d['label']}:** {d.get('note', '')}")
        st.markdown(f"##### {I['question']} Still needed from you")
        for q in f.get("missing_info") or ["—"]:
            st.markdown(f"- {q}")
        st.markdown(f"##### {I['phone']} Help lines")
        for h in analysis.get("helplines", []):
            st.markdown(f"- {h}")
    st.download_button("Download case file (.docx)", engine.to_docx(case["title"], engine.case_summary_md(case, analysis)),
                       file_name="case_file.docx", icon=I["download"])

# ------------------------------------------------------------------ EVIDENCE VAULT
with tab_vault:
    st.markdown(f"#### {I['search']} Find a file fast")
    st.caption("Describe it however you remember - e.g. *\"the screenshot of the office guy who refused my salary\"*. Type or say it.")
    q1, q2 = st.columns([4, 1])
    query = q1.text_input("What do you need?", key="vault_q", label_visibility="collapsed",
                          placeholder="e.g. lease agreement / landlord's number / audio of the HR call")
    all_cases = q2.toggle("All cases", value=False)
    spoken = st.audio_input("...or say it", key="vault_audio")
    if spoken is not None and st.session_state.get("vault_audio_done") != spoken.file_id and need_llm():
        with st.spinner("Listening..."):
            try:
                st.session_state.vault_spoken = llm.transcribe(spoken.getvalue(), "query.wav")
            except Exception as e:  # noqa: BLE001
                st.error(f"Could not transcribe: {e}", icon=I["warn"])
        st.session_state.vault_audio_done = spoken.file_id
    q = query or st.session_state.get("vault_spoken", "")
    if spoken is not None and st.session_state.get("vault_spoken"):
        st.markdown(f"{I['mic']} _\"{st.session_state.vault_spoken}\"_")

    if q:
        targets = [store.load(c["id"], ROOT) for c in store.list_cases(ROOT) if c["n_files"]] if all_cases else [case]
        quick = st.empty()
        lex = vault.lexical_search(q, targets, k=4)
        if lex:
            quick.caption("Quick matches: " + " · ".join(file_label(r["file"]) for r in lex) + "  (AI is refining...)")
        results, interp = [], []
        for t in targets[:6]:
            out = vault.smart_search(q, t, llm)
            results += out["results"]
            interp.append(out["interpretation"])
        quick.empty()
        results.sort(key=lambda r: -r["score"])
        if interp and interp[0]:
            st.caption(f"Understood as: {interp[0]}")
        if not results:
            st.info("Nothing matched. Try other words (who, what kind of file, roughly when).", icon=I["search"])
        for i, r in enumerate(results):
            src = store.load(r["case_id"], ROOT) if r["case_id"] != case["id"] else case
            conf = r["score"]
            head = f"{file_label(r['file'])}  ·  {int(conf * 100) if conf <= 1 else conf}% match" + (f"  ·  case: {r['case_title']}" if all_cases else "")
            if i == 0:
                with st.container(border=True):
                    st.markdown(f"{I['best']} **Best match:** {head}  \n_{r['reason']}_")
                    render_file(src, r["file"], ctx="best", big=True)
            else:
                with st.expander(f"{head} — {r['reason']}"):
                    render_file(src, r["file"], ctx=f"res{i}")

    st.divider()
    st.markdown(f"#### {I['upload']} Add to vault")
    up_c1, up_c2 = st.columns([3, 2])
    with up_c1:
        ups = st.file_uploader("Photos, screenshots, PDFs, recordings", type=UPLOAD_TYPES, accept_multiple_files=True, key="vault_up")
        note = st.text_input("Short note (who/what is this?)", key="vault_note", placeholder="e.g. chat with Rohit from HR, 3 Sept")
        if st.button("Save to vault", icon=I["save"], disabled=not ups) and need_llm():
            with st.spinner(f"Indexing {len(ups)} file(s)..."):
                for u in ups:
                    vault.ingest(case, llm, u.name, u.getvalue(), note=note)
            st.rerun()
    with up_c2:
        nt = st.text_input("Quick note title", placeholder="e.g. Landlord phone & address", key="note_t")
        nb = st.text_area("Note", placeholder="Ramesh Gupta, 98xxxxxx12, B-14 Lajpat Nagar", key="note_b", height=90)
        if st.button("Save note", icon=I["note"], disabled=not (nt and nb)):
            vault.add_note(case, nt, nb)
            st.rerun()

    st.divider()
    st.markdown(f"#### {I['vault']} All files in this case ({len(case['files'])})")
    cats = sorted({(f.get("ai") or {}).get("category", "other") for f in case["files"]})
    pick = st.multiselect("Filter", cats, format_func=lambda c: c.replace("_", " ")) if cats else []
    for f in reversed(case["files"]):
        ai = f.get("ai") or {}
        if pick and ai.get("category") not in pick:
            continue
        with st.expander(file_label(f) + (f"  ·  {f['user_note'][:40]}" if f.get("user_note") else "")):
            a, b = st.columns([2, 3])
            with a:
                render_file(case, f, ctx="list")
            with b:
                if ai:
                    st.markdown(f"**{ai.get('title', '')}**  \n{ai.get('description', '')}")
                    if ai.get("people"):
                        st.markdown("**People:** " + ", ".join(f"{p.get('name') or '?'} ({p.get('role') or '?'})" for p in ai["people"] if isinstance(p, dict)))
                    if ai.get("key_text"):
                        st.markdown(f"**Key text:** _{ai['key_text'][:400]}_")
                    if ai.get("tags"):
                        st.caption(f"{I['tag']} " + ", ".join(ai["tags"]))
                elif f.get("ai_error"):
                    st.caption(f"AI indexing failed: {f['ai_error'][:160]}")
                    if st.button("Retry indexing", icon=I["retry"], key=f"ri_{f['id']}") and need_llm():
                        with st.spinner("Indexing..."):
                            f["ai_error"] = None
                            vault.analyze_file(case, f, store.file_path(case, f).read_bytes(), llm)
                            store.save(case)
                        st.rerun()
                st.caption(f"Added {f['uploaded_at']} via {f['source']}")
                new_note = st.text_input("Your note", value=f.get("user_note") or "", key=f"note_{f['id']}")
                bc1, bc2, bc3 = st.columns(3)
                if bc1.button("Save note", icon=I["save"], key=f"sn_{f['id']}"):
                    f["user_note"] = new_note
                    store.save(case)
                    st.rerun()
                if f["kind"] in ("image", "pdf", "docx", "text") and bc2.button("Explain", icon=I["explain"], key=f"ex_{f['id']}") and need_llm():
                    with st.spinner("Reading the document..."):
                        engine.explain_file(case, llm, f)
                    st.rerun()
                if bc3.button("Remove", icon=I["delete"], key=f"rm_{f['id']}"):
                    store.file_path(case, f).unlink(missing_ok=True)
                    case["files"] = [x for x in case["files"] if x["id"] != f["id"]]
                    store.save(case)
                    st.rerun()
                if f.get("explanation"):
                    st.markdown(f["explanation"]["text"])
                    render_citations(f["explanation"]["citations"])
                    render_warnings(f["explanation"]["warnings"])

# ------------------------------------------------------------------ DOCUMENTS
with tab_docs:
    st.markdown(f"#### {I['draft']} Draft a document from your case file")
    st.caption("Uses only facts from your case file. Anything missing is marked **[FILL: ...]** - never invented.")
    d1, d2 = st.columns([3, 1])
    doc_type = d1.selectbox("What do you need?", list(engine.DOC_TYPES))
    lang = d2.selectbox("Language", list(dict.fromkeys(["English", "Hindi", case["facts"].get("language") or "English"])))
    extra = st.text_input("Anything specific? (optional)", placeholder="e.g. also ask for 12% interest; keep it short")
    if st.button("Draft it", icon=I["draft"], type="primary") and need_llm():
        if not case["messages"]:
            st.info("Tell Nyaya about your problem in the Talk tab first.", icon=I["talk"])
        else:
            with st.spinner("Drafting..."):
                engine.draft_document(case, llm, doc_type, lang, extra)
            st.rerun()
    for doc in reversed(case["documents"]):
        with st.expander(f"{doc['id']} · {doc['type']} · {doc['created']}", icon=I["docs"], expanded=doc is case["documents"][-1]):
            if doc.get("placeholders"):
                st.error(f"Fill these {len(doc['placeholders'])} blanks before sending: " + ", ".join(dict.fromkeys(doc["placeholders"])), icon=I["warn"])
            render_warnings(doc.get("warnings"))
            edited = st.text_area("Edit", value=doc["content"], height=420, key=f"doc_{doc['id']}")
            e1, e2, e3, e4 = st.columns(4)
            if e1.button("Save edits", icon=I["save"], key=f"save_{doc['id']}"):
                doc["content"] = edited
                store.save(case)
                st.rerun()
            e2.download_button(".docx", engine.to_docx(doc["type"], edited), file_name=f"{doc['id']}_{doc['type'][:30]}.docx",
                               icon=I["download"], key=f"dx_{doc['id']}")
            e3.download_button(".txt", edited.encode("utf-8"), file_name=f"{doc['id']}.txt", icon=I["download"], key=f"tx_{doc['id']}")
            if e4.button("Save to vault", icon=I["vault"], key=f"tv_{doc['id']}"):
                rec = vault.ingest(case, None, f"{doc['id']}_{doc['type'][:30]}.docx", engine.to_docx(doc["type"], edited),
                                   note=f"Generated: {doc['type']}", source="generated", analyze=False)
                rec["text"] = edited
                rec["ai"] = {"title": f"{doc['type']} (draft {doc['id']})", "category": "generated_document",
                             "description": edited[:300], "people": [], "dates": [], "amounts": [], "key_text": "",
                             "tags": vault._tokens(doc["type"])}
                store.save(case)
                st.toast("Saved to vault", icon=I["ok"])

# ------------------------------------------------------------------ PRACTICE
with tab_practice:
    role = engine.other_side_role(case)
    st.markdown(f"#### {I['practice']} Practise talking to **{role}**")
    st.caption("The AI plays the other side and pushes back with common excuses. Practise staying calm and pointing to your proof. "
               "Click *Get feedback* when you're done.")
    for m in case["practice"]["messages"]:
        with st.chat_message("user" if m["role"] == "user" else "assistant", avatar=I["user"] if m["role"] == "user" else I["other_side"]):
            st.markdown(m["content"])
    p_in = st.chat_input(f"Say something to {role}...", key="practice_input")
    if p_in and need_llm():
        with st.spinner("..."):
            engine.practice_reply(case, llm, p_in)
        st.rerun()
    pc1, pc2 = st.columns(2)
    if pc1.button("Get feedback", icon=I["feedback"], disabled=not case["practice"]["messages"]) and need_llm():
        with st.spinner("Reviewing your practice..."):
            engine.practice_feedback(case, llm)
        st.rerun()
    if pc2.button("Start over", icon=I["restart"]):
        case["practice"] = {"messages": [], "feedback": None}
        store.save(case)
        st.rerun()
    if case["practice"].get("feedback"):
        st.markdown("---")
        st.markdown(case["practice"]["feedback"]["text"])
        render_citations(case["practice"]["feedback"]["citations"])
