"""Case persistence: one folder per case -> case.json + files/ (the evidence vault)."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(os.getenv("DATA_DIR") or Path(__file__).resolve().parent.parent / "data" / "cases")


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def empty_facts() -> dict:
    return {
        "case_title": None,            # AI-written short title (like a chat title)
        "problem_type": None,          # deposit | salary | consumer | notice_received | other
        "summary": "",
        "user": {"name": None, "phone": None, "address": None},
        "location": {"city": None, "state": None},
        "parties": [],                 # [{name, role, relation_to_user, phone, address, aliases[], description}]
        "timeline": [],                # [{date, event, source}]
        "amount_in_dispute_inr": None,
        "consideration_paid_inr": None,
        "cause_of_action_date": None,
        "notice_reply_deadline": None,
        "evidence": [],                # [{item, status: uploaded|mentioned|needed, file_ids[]}]
        "missing_info": [],            # [str] questions still open, most important first
        "risk_flags": [],
        "user_goal": None,
        "language": None,
    }


def new_case(title: str = "New case", base: Path | None = None) -> dict:
    cid = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:4]
    case = {
        "id": cid, "title": title, "created": now(), "updated": now(),
        "messages": [], "facts": empty_facts(), "files": [], "documents": [],
        "practice": {"messages": [], "feedback": None}, "title_locked": False,
    }
    save(case, base)
    return case


def case_dir(cid: str, base: Path | None = None) -> Path:
    d = (base or DATA_DIR) / cid
    (d / "files").mkdir(parents=True, exist_ok=True)
    return d


def user_root(user_id: str | None) -> Path:
    """Signed-in users get their own folder; guests (no sign-in configured) use the shared root."""
    if not user_id:
        return DATA_DIR
    return DATA_DIR / "users" / hashlib.sha256(user_id.lower().encode()).hexdigest()[:20]


def _root(case: dict, base: Path | None) -> Path | None:
    return base or (Path(case["_root"]) if case.get("_root") else None)


def save(case: dict, base: Path | None = None) -> None:
    case["updated"] = now()
    root = _root(case, base)
    p = case_dir(case["id"], root) / "case.json"
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps({k: v for k, v in case.items() if k != "_root"}, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(p)
    if root:
        case["_root"] = str(root)


def load(cid: str, base: Path | None = None) -> dict:
    case = json.loads((case_dir(cid, base) / "case.json").read_text(encoding="utf-8"))
    if base:
        case["_root"] = str(base)
    return case


def list_cases(base: Path | None = None) -> list[dict]:
    root = base or DATA_DIR
    root.mkdir(parents=True, exist_ok=True)
    out = []
    for d in sorted(root.iterdir(), reverse=True):
        f = d / "case.json"
        if f.exists():
            try:
                c = json.loads(f.read_text(encoding="utf-8"))
                out.append({"id": c["id"], "title": c["title"], "updated": c["updated"], "n_files": len(c["files"]),
                            "n_msgs": len(c["messages"])})
            except Exception:  # noqa: BLE001
                continue
    return sorted(out, key=lambda c: c["updated"], reverse=True)  # most recently active first, like chat apps


def delete_case(cid: str, base: Path | None = None) -> None:
    shutil.rmtree((base or DATA_DIR) / cid, ignore_errors=True)


def file_path(case: dict, f: dict, base: Path | None = None) -> Path:
    return case_dir(case["id"], _root(case, base)) / "files" / f["stored_name"]


def next_file_id(case: dict) -> str:
    n = max([int(f["id"][1:]) for f in case["files"]] or [0]) + 1
    return f"F{n}"
