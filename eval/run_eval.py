"""Run the test cases end-to-end and write UNEDITED raw outputs + an automatic scorecard.

  python eval/run_eval.py                       # everything, default provider (.env)
  python eval/run_eval.py --provider groq       # same tests on another model (swap check)
  python eval/run_eval.py --only retrieval
  python eval/run_eval.py --cases C10_trap_ipc C11_trap_case_law

Output: outputs/run_<timestamp>_<provider>/{<case>.md, retrieval.md, results.json, SUMMARY.md}
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8")
from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")

ap = argparse.ArgumentParser()
ap.add_argument("--provider")
ap.add_argument("--model")
ap.add_argument("--only", choices=["conversation", "retrieval"])
ap.add_argument("--cases", nargs="*")
ap.add_argument("--pause", type=float, default=4.0, help="seconds between LLM-heavy steps (free-tier rate limits)")
args = ap.parse_args()

provider = args.provider or os.getenv("LLM_PROVIDER", "gemini")
RUN = ROOT / "outputs" / f"run_{datetime.now():%Y%m%d_%H%M%S}_{provider}"
os.environ["DATA_DIR"] = str(RUN / "cases")  # isolated case store for this run

from core import engine, store, vault  # noqa: E402
from core.llm import LLM  # noqa: E402

llm = LLM.from_env(args.provider, args.model)
if not llm.configured:
    sys.exit(f"No API key for {llm.provider}. Put it in .env")
TESTS = json.loads((ROOT / "eval" / "test_cases.json").read_text(encoding="utf-8"))
LEVEL = {"none": 0, "suggested": 1, "required": 2}
RUN.mkdir(parents=True, exist_ok=True)


def script_of(text: str) -> str:
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return "latin"
    dev = sum("ऀ" <= c <= "ॿ" for c in letters) / len(letters)
    tam = sum("஀" <= c <= "௿" for c in letters) / len(letters)
    return "devanagari" if dev > 0.3 else "tamil" if tam > 0.3 else "latin"


def check(case: dict, exp: dict, replies: list[dict]) -> dict:
    facts, an = case["facts"], case.get("analysis", {})
    last = replies[-1]["content"] if replies else ""
    all_warn = [w for r in replies for w in r.get("warnings", [])]
    res = {}
    # a case can never pass if the model did not actually answer / extraction failed
    res["model_answered"] = not any("AI model is unavailable" in r["content"] for r in replies) and not case.get("errors")
    if "problem_type" in exp:
        res["problem_type"] = facts.get("problem_type") == exp["problem_type"]
    lvl = LEVEL.get(an.get("referral", {}).get("level", "none"), 0)
    if "referral_min" in exp:
        res["referral_min"] = lvl >= LEVEL[exp["referral_min"]]
    if "referral_max" in exp:
        res["referral_max"] = lvl <= LEVEL[exp["referral_max"]]
    if "script" in exp:
        res["language_script"] = script_of(last) == exp["script"]
    if exp.get("asks_question"):
        res["asks_question"] = "?" in last
    if exp.get("asks_upload"):
        res["asks_upload"] = bool(re.search(r"upload|attach|📎|share (a |the )?(photo|copy|screenshot)", last, re.I))
    if "must_mention_any" in exp:
        res["mentions"] = any(m.lower() in last.lower() for m in exp["must_mention_any"])
    if "forum_contains" in exp:
        res["forum"] = any(exp["forum_contains"] in f["forum"] for f in an.get("forum", []))
    if exp.get("no_repealed_citation"):
        res["no_repealed_citation"] = not any("repealed" in w for w in all_warn)
    if exp.get("no_unverified_case_law"):
        res["no_unverified_case_law"] = not any("court case" in w for w in all_warn)
    res["zero_validator_warnings"] = len(all_warn) == 0  # informational: did the model stay inside the KB?
    return res


def run_conversations() -> list[dict]:
    rows = []
    for tc in TESTS["conversation_cases"]:
        if args.cases and tc["id"] not in args.cases:
            continue
        print(f"[conv] {tc['id']} ...", flush=True)
        case = store.new_case(tc["id"])
        replies, t0 = [], time.time()
        for turn in tc["turns"]:
            replies.append(engine.process_turn(case, llm, turn))
            time.sleep(args.pause)
        res = check(case, tc["expect"], replies)
        scored = {k: v for k, v in res.items() if k != "zero_validator_warnings"}
        rows.append({"id": tc["id"], "checks": res, "passed": all(scored.values()), "seconds": round(time.time() - t0, 1)})
        md = [f"# {tc['id']}", f"model: {llm.provider}/{llm.model}", "", "## Transcript (raw, unedited)"]
        for m in case["messages"]:
            md += [f"### {m['role'].upper()}", m.get("raw", m["content"]), ""]
            if m["role"] == "assistant":
                md += [f"_answered by:_ {m.get('model')}", f"_citations:_ {m.get('citations')}", f"_validator warnings:_ {m.get('warnings')}", ""]
        md += ["## Extracted case file", "```json", json.dumps(case["facts"], ensure_ascii=False, indent=2), "```",
               "## Rules engine output", "```json", json.dumps(case.get("analysis"), ensure_ascii=False, indent=2), "```",
               "## Checks", "```json", json.dumps(res, indent=2), "```"]
        (RUN / f"{tc['id']}.md").write_text("\n".join(md), encoding="utf-8")
    return rows


def run_retrieval() -> list[dict]:
    R = TESTS["retrieval"]
    print("[retrieval] building evidence vault ...", flush=True)
    case = store.new_case("Retrieval test")
    for t in R["setup_turns"]:
        engine.process_turn(case, llm, t)
    ev = ROOT / "samples" / "evidence"
    for f in R["files"]:
        p = ev / f["file"]
        if not p.exists():
            print(f"  missing sample {p.name} - run samples/make_samples.py")
            continue
        rec = vault.ingest(case, llm, p.name, p.read_bytes(), note=f["note"])
        print(f"  {rec['id']} {p.name}: {(rec.get('ai') or {}).get('title') or rec.get('ai_error')}")
        time.sleep(args.pause)
    for n in R["notes"]:
        vault.add_note(case, n["title"], n["text"])

    rows, md = [], ["# Evidence-vault retrieval test", f"model: {llm.provider}/{llm.model}", "", "## Vault index cards"]
    for f in case["files"]:
        md += [f"- **{f['id']} {f['filename']}** -> {json.dumps(f.get('ai'), ensure_ascii=False)}"]
        if f.get("transcript"):
            md += [f"  - transcript: {f['transcript']}"]
    md += ["", "## Queries"]
    for q in R["queries"]:
        lex = vault.lexical_search(q["q"], [case])
        smart = vault.smart_search(q["q"], case, llm)
        lex_names = [r["file"]["filename"] for r in lex]
        ai_names = [r["file"]["filename"] for r in smart["results"]]
        row = {"query": q["q"], "expect": q["expect"], "lexical_top1": lex_names[:1] == [q["expect"]],
               "lexical_top3": q["expect"] in lex_names[:3], "ai_top1": ai_names[:1] == [q["expect"]],
               "ai_top3": q["expect"] in ai_names[:3], "ai_mode": smart["mode"]}
        rows.append(row)
        md += [f"### \"{q['q']}\"", f"- expected: `{q['expect']}`", f"- AI interpretation: {smart['interpretation']}",
               f"- AI ranking: {[(r['file']['filename'], r['score'], r['reason']) for r in smart['results']]}",
               f"- keyword ranking: {[(n, r['score']) for n, r in zip(lex_names, lex)]}", ""]
        time.sleep(args.pause)
    (RUN / "retrieval.md").write_text("\n".join(md), encoding="utf-8")

    return rows


conv = run_conversations() if args.only != "retrieval" else []
retr = run_retrieval() if args.only != "conversation" else []
(RUN / "results.json").write_text(json.dumps({"model": f"{llm.provider}/{llm.model}", "conversation": conv, "retrieval": retr}, indent=2, ensure_ascii=False), encoding="utf-8")

S = [f"# Eval summary - {llm.provider}/{llm.model} - {datetime.now():%Y-%m-%d %H:%M}", ""]
if conv:
    S += [f"## Conversation cases: {sum(r['passed'] for r in conv)}/{len(conv)} passed", "", "| case | pass | failed checks | KB-clean |", "|---|---|---|---|"]
    for r in conv:
        failed = [k for k, v in r["checks"].items() if not v and k != "zero_validator_warnings"]
        S.append(f"| {r['id']} | {'✅' if r['passed'] else '❌'} | {', '.join(failed) or '-'} | {'✅' if r['checks']['zero_validator_warnings'] else '⚠️'} |")
if retr:
    n = len(retr)
    S += ["", f"## Evidence retrieval ({n} queries)",
          f"- AI re-rank: top-1 {sum(r['ai_top1'] for r in retr)}/{n}, top-3 {sum(r['ai_top3'] for r in retr)}/{n}",
          f"- Keyword only (offline fallback): top-1 {sum(r['lexical_top1'] for r in retr)}/{n}, top-3 {sum(r['lexical_top3'] for r in retr)}/{n}", ""]
    for r in retr:
        S.append(f"- {'✅' if r['ai_top1'] else '❌'} ai / {'✅' if r['lexical_top1'] else '❌'} kw  \"{r['query'][:70]}\" -> {r['expect']}")
(RUN / "SUMMARY.md").write_text("\n".join(S), encoding="utf-8")
print("\n".join(S))
print(f"\nRaw outputs: {RUN}")
