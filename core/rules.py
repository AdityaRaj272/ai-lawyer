"""Deterministic rules: things that must be right are computed in code, not generated.

- which forum (consumer pecuniary limits)
- deadlines (limitation periods) and days left
- when the person MUST / SHOULD see a real lawyer
- the evidence checklist per problem type
"""
from __future__ import annotations

import re
from datetime import date, datetime, timedelta

SCOPE = {
    "deposit": "Security deposit not returned (rented home)",
    "salary": "Unpaid / delayed salary or final settlement",
    "consumer": "Refund / defective product / bad service (incl. online)",
    "notice_received": "Understanding & replying to a notice you received",
}

EVIDENCE_CHECKLIST = {
    "deposit": [
        "Rent / leave-and-licence agreement",
        "Proof the deposit was paid (bank transfer, UPI screenshot, receipt)",
        "Rent payment records (last few months)",
        "Proof of move-out date / key handover",
        "Photos or video of the flat condition at move-out",
        "Chats/emails where you asked for the deposit back (and their replies)",
        "Landlord's full name, phone number and address (photo/ID if you have it)",
    ],
    "salary": [
        "Offer letter / appointment letter",
        "Salary slips (last paid months)",
        "Bank statement showing the last salary credit",
        "Proof you worked in the unpaid period (attendance, emails, work logs)",
        "Resignation / termination / relieving letter",
        "Chats/emails where you asked for your salary (and their replies)",
        "Employer's registered name & address; HR/manager's name, phone (photo/ID card if you have it)",
    ],
    "consumer": [
        "Invoice / order ID / booking confirmation",
        "Payment proof (card/UPI/bank statement)",
        "Photos/video of the defect or problem",
        "Complaint ticket numbers + chats/emails with customer care",
        "Seller / company name and address (from invoice or website)",
        "Warranty card / terms promised at purchase",
    ],
    "notice_received": [
        "The notice itself (all pages, both sides)",
        "Envelope / courier slip showing the date you received it",
        "The agreement or transaction the notice is about",
        "Your proof for your side (payments, chats, receipts)",
    ],
}

# risk flag -> (level, reason)
RISK_FLAGS = {
    "user_accused_of_crime": ("required", "Someone has accused you of a crime / filed a police complaint against you."),
    "police_or_arrest": ("required", "Police involvement against you (summons, questioning, arrest)."),
    "court_summons": ("required", "You have received court summons / a court case is already filed - court dates are binding."),
    "violence_or_threat": ("required", "Threats or violence: your safety comes first - call 112 if in danger."),
    "family_or_matrimonial": ("required", "Family / marriage / custody matters are outside this app's scope."),
    "property_title_or_eviction_suit": ("required", "Property ownership or an eviction case needs a lawyer."),
    "sexual_harassment": ("required", "Sexual harassment: complain to the Internal Committee / police; get specialised help (women's helpline 181)."),
    "government_party": ("suggested", "The other side is a Government body (special notice rules apply - CPC s.80)."),
    "other_party_has_lawyer": ("suggested", "The other side already has a lawyer."),
    "cheque_bounce": ("suggested", "Cheque-bounce cases are criminal proceedings with strict deadlines."),
    "large_amount": ("suggested", "The amount involved is large (over Rs 20 lakh)."),
}

KEYWORD_FLAGS = [
    (r"\b(fir against me|complaint against me|arrest|police (called|came|notice) me|summon)", "police_or_arrest"),
    (r"\b(court summons|summons from court|case filed against me|next hearing)", "court_summons"),
    (r"\b(threatened|threatening|threat to|beat me|hit me|maarne|maarunga|dhamki|will kill)", "violence_or_threat"),
    (r"\b(divorce|custody of|dowry|talaq|domestic violence|matrimonial|maintenance from my (husband|wife))", "family_or_matrimonial"),
    (r"\b(sexual|harass(ed|ment) .*(touch|sexual)|posh)", "sexual_harassment"),
    (r"\b(cheque bounce|cheque (was )?dishonou?r|section 138)", "cheque_bounce"),
]


def _parse_date(s) -> date | None:
    if not s or not isinstance(s, str):
        return None
    s = s.strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y-%m", "%d %B %Y", "%d %b %Y", "%B %Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    m = re.search(r"(\d{4})-(\d{2})(?:-(\d{2}))?", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3) or 1))
    return None


def _add_years(d: date, years: int) -> date:
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        return d + timedelta(days=365 * years)


def consumer_forum(paid: float | None) -> dict | None:
    if not paid:
        return None
    if paid <= 50_00_000:
        name = "District Consumer Commission"
    elif paid <= 2_00_00_000:
        name = "State Consumer Commission"
    else:
        name = "National Consumer Commission (NCDRC)"
    fee = "No filing fee (paid amount up to Rs 5 lakh)" if paid <= 5_00_000 else "Filing fee applies - check the fee table on e-Jagriti"
    return {"forum": name, "basis": "cpa-jurisdiction-rules-2021", "fee": fee, "fee_basis": "cpa-fee"}


def analyze(facts: dict, user_text: str = "", today: date | None = None) -> dict:
    today = today or date.today()
    pt = facts.get("problem_type") or "unknown"
    out: dict = {
        "problem_type": pt,
        "in_scope": pt in SCOPE,
        "scope_note": SCOPE.get(pt, "Not one of the 4 problem types this app covers in depth - general guidance only."),
        "forum": [],
        "deadlines": [],
        "referral": {"level": "none", "reasons": []},
        "checklist": EVIDENCE_CHECKLIST.get(pt, []),
        "helplines": ["NALSA free legal aid: 15100", "Police emergency: 112"],
    }
    if pt == "consumer":
        out["helplines"].insert(0, "National Consumer Helpline: 1915")
    if pt not in SCOPE and pt not in ("unknown", None):
        out["referral"] = {"level": "suggested", "reasons": ["This kind of problem is outside what this app covers in depth."]}

    amount = facts.get("amount_in_dispute_inr") or 0
    paid = facts.get("consideration_paid_inr") or amount
    cause = _parse_date(facts.get("cause_of_action_date"))

    # ---- forum ----
    if pt == "consumer":
        f = consumer_forum(paid)
        if f:
            out["forum"].append(f)
        out["forum"].insert(0, {"forum": "National Consumer Helpline (free, pre-litigation)", "basis": "nch"})
        out["forum"].append({"forum": "File online at e-jagriti.gov.in", "basis": "ejagriti"})
    elif pt == "salary":
        out["forum"].append({"forum": "Labour Department / wage authority of your State (claim for unpaid wages)", "basis": "cow-45"})
        out["forum"].append({"forum": "Legal notice to the employer; civil court for recovery if the wage authority route is not available to you (ask a lawyer)", "basis": "legal-notice"})
    elif pt == "deposit":
        out["forum"].append({"forum": "Legal notice first; then civil court (money recovery suit) in the area of the flat", "basis": "rent-state-law"})
        out["forum"].append({"forum": "Lok Adalat / DLSA mediation (free, faster)", "basis": "nalsa"})

    # ---- deadlines ----
    def add_deadline(label, years, basis):
        if cause:
            last = _add_years(cause, years)
            out["deadlines"].append({"label": label, "last_date": last.isoformat(), "days_left": (last - today).days, "basis": basis,
                                     "counted_from": cause.isoformat()})
        else:
            out["deadlines"].append({"label": label, "last_date": None, "days_left": None, "basis": basis,
                                     "note": f"{years} years from the date the refund/payment was due or refused - tell me that date to compute it."})

    if pt == "consumer":
        add_deadline("File consumer complaint", 2, "cpa-69")
    elif pt == "deposit":
        add_deadline("File civil suit for deposit", 3, "limitation-money")
    elif pt == "salary":
        add_deadline("File wage claim", 3, "cow-45")
    elif pt == "notice_received":
        reply_by = _parse_date(facts.get("notice_reply_deadline"))
        if reply_by:
            out["deadlines"].append({"label": "Respond to the notice by", "last_date": reply_by.isoformat(),
                                     "days_left": (reply_by - today).days, "basis": "notice-reply"})

    # ---- referral ----
    flags = set(facts.get("risk_flags") or [])
    for pattern, flag in KEYWORD_FLAGS:
        if re.search(pattern, user_text or "", re.I):
            flags.add(flag)
    if (amount or 0) > 20_00_000:
        flags.add("large_amount")
    reasons, level = [], out["referral"]["level"]
    for f in sorted(flags):
        if f in RISK_FLAGS:
            lv, why = RISK_FLAGS[f]
            reasons.append(why)
            if lv == "required":
                level = "required"
            elif level == "none":
                level = "suggested"
    for d in out["deadlines"]:
        if d.get("days_left") is not None and d["days_left"] < 0:
            reasons.append(f"The usual time limit ('{d['label']}') may already have passed - a lawyer can check if the delay can be condoned.")
            level = "required"
        elif d.get("days_left") is not None and d["days_left"] < 30 and level == "none":
            reasons.append(f"Deadline '{d['label']}' is less than 30 days away.")
            level = "suggested"
    if reasons:
        out["referral"] = {"level": level, "reasons": out["referral"]["reasons"] + reasons}
    out["flags"] = sorted(flags)
    return out
