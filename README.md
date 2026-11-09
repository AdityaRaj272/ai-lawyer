# Nyaya: AI legal help for everyday problems in India

**Live app:** https://nyaya-ai-lawyer.streamlit.app

A conversational assistant that takes your problem by text or voice, in your own language, and turns it into a case file, evidence and documents you can act on. It covers four problems in depth:

| Covered in depth | Not covered (it refers you to a lawyer or free legal aid) |
|---|---|
| Security deposit not returned | Criminal cases against you, police or arrest |
| Unpaid or delayed salary, final settlement | Family, divorce, custody |
| Consumer refunds, defects, bad service (online too) | Property title, eviction suits |
| Understanding or replying to a notice you received | Court summons and ongoing litigation |

## Run it

```bash
pip install -r requirements.txt
cp .env.example .env          # add GEMINI_API_KEY (free: https://aistudio.google.com/apikey)
python samples/make_samples.py   # optional: fictional evidence files for the demo/eval
streamlit run app.py
python eval/run_eval.py          # test cases -> outputs/run_*/ (raw outputs + scorecard)
```

**To swap the model**, set `LLM_PROVIDER=groq` (or `openrouter`, `openai`, `ollama`, `custom`) in `.env`, or use the sidebar. Every provider goes through the OpenAI-compatible API ([core/llm.py](core/llm.py)). Any other OpenAI-compatible endpoint works with `custom` plus `LLM_BASE_URL`, `LLM_API_KEY` and `LLM_MODEL`.

### Optional: Sign in with Google

Without this, the app runs in **guest mode**: no login, and cases are stored on the machine. With it, every Google account gets its own private set of cases and evidence (stored under `data/cases/users/<hashed email>/`).

1. Go to [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services. On the **OAuth consent screen**, choose External and add yourself as a test user.
2. Go to **Credentials → Create credentials → OAuth client ID → Web application**. Under *Authorized redirect URIs*, add `http://localhost:8501/oauth2callback` (and `https://<your-app>.streamlit.app/oauth2callback` if you deploy).
3. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`. Fill in `client_id`, `client_secret` and a random `cookie_secret`, then restart the app.

On Streamlit Community Cloud, paste the same `[auth]` block into the app's *Secrets* settings.

## What it does

1. **Talk.** Type, record voice, or attach files in the chat box. It replies in your language and script (English, Hinglish, Hindi, Tamil and others). Each turn it asks up to 3 specific questions for missing details (exact dates, full names, addresses, amounts) and asks you to upload proof, plus the other party's phone, address and photo or ID.
2. **Case file.** Structured facts update after every message: parties and their aliases, timeline, amounts, and evidence status (in vault / you have it / needed). The "where you stand" section (forum, deadlines with days left, lawyer referral) is computed by rules in code. Exports to .docx.
3. **Evidence vault.** Every upload gets an AI-made index card: OCR of screenshots, transcripts of audio, extracted text from PDFs and DOCX, who is in it, dates, verbatim key lines, and tags. You can find a file from a vague, rambling or spoken description, for example *"the screenshot of the guy from the office who told me to f\*\*\* off about my salary"*. Retrieval works in two stages:
   - instant keyword match, with synonyms and party aliases resolved from the case (works offline)
   - an LLM re-rank over the whole case catalog, which works out that "the guy from the office" means Rohit, the HR manager

   The best match opens full-screen with a download button, so you can show it at a police station or office. Typed notes ("landlord phone and address") are vault items too. You can search across all cases.
4. **Documents.** Legal notice, consumer complaint, grievance email, labour complaint, reply to a notice, police complaint, or a case brief for a lawyer. Each is drafted only from the case file; anything missing becomes `[FILL: …]`. Annexures refer to vault files. You can edit the draft, download it as PDF (Hindi renders correctly), Word or text, and save it back to the vault. The private "notes for you" (how to send it, what to keep) are shown on screen but never included in the downloaded files.
5. **Explain a document.** Any notice or letter in the vault can be explained: what it says, deadlines, how serious it is, what to do, and whether you need a lawyer.
6. **Practice.** The AI plays the landlord, HR or seller with the excuses they usually give, then coaches you on your arguments.

## How it avoids inventing laws (and what stays in code)

| Job | Handled by |
|---|---|
| Understanding messy speech, pulling out facts, explaining simply, drafting, role-play, file indexing | LLM |
| Which law exists and what it says | [kb/legal_kb.json](kb/legal_kb.json): 27 entries, each checked against the bare-act text or at least two credible sources, with the sources listed in `verified_by`. Four entries that couldn't be verified were removed. |
| Forum (consumer pecuniary limits), limitation deadlines, when a lawyer is required | [core/rules.py](core/rules.py): deterministic |
| Checking every answer | [core/kb.py](core/kb.py) `validate()`: the model may cite only `[[KB:id]]` tags. Unknown tags are removed. Any raw "Section N" not in the KB, any section number of IPC/CrPC/Evidence Act (repealed 1 July 2024), and any "X vs Y" case name is flagged under the answer. |

## Known limits

- The KB was verified on 2026-11-08 from public bare-act reproductions and secondary sources, not by a lawyer. Its summaries are plain-language paraphrases. Tenancy law is State-specific, and the Model Tenancy Act applies only where a State has adopted it.
- The validator catches citations that look like citations. It cannot catch a wrong *paraphrase* of a real law.
- **Free tier:** Gemini allows only 5 requests per minute per model. [core/llm.py](core/llm.py) throttles per model, waits the retry time Gemini returns, and switches to `gemini-3.5-flash-lite` (which has its own quota) when the main model is at its limit. Each answer records which model produced it. A chat turn costs 2 calls and each upload 1. `gemini-flash-latest` and `gemini-3.8-flash` are thinking models, about 60 s per call versus about 3 s for `gemini-3.5-flash`, so they aren't the default.
- Voice transcription quality depends on the model (Gemini sends audio inline; Groq uses Whisper).
- Storage is local JSON plus files, with no login or encryption. That's fine for a prototype. In production this would need auth and encryption, because the data is sensitive.
- Streamlit Community Cloud storage is temporary, so uploaded files disappear when the app restarts.
- Scanned PDFs without a text layer aren't read unless uploaded as images.
