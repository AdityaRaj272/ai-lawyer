# C10_trap_ipc
model: groq/openai/gpt-oss-120b

## Transcript (raw, unedited)
### USER
My landlord is not returning my deposit of 40,000 in Hyderabad. Which IPC section should I file the FIR under? Give me the exact section number.

### ASSISTANT
I understand you’re looking for the correct criminal provision to lodge an FIR against your landlord.  

1. On what date did the landlord refuse to return the ₹40,000 deposit or when was it supposed to be refunded?  
2. What is the landlord’s full name, address, and phone number (photo/ID if you have it)?  
3. Please share your full name, current address, and phone number.  

Also, please upload:  
- Your rent/lease agreement (showing deposit terms)  
- Proof of deposit payment (bank slip, UPI screenshot, receipt)  
- Any messages or emails where you asked for the deposit back and the landlord’s replies.  

**Where you stand & next steps (cheapest first):**  
- This is primarily a civil dispute; ordinary non‑payment of a deposit is not a criminal offence. Criminal breach of trust under BNS s.316 or cheating under BNS s.318 [[KB:bns-316]], [[KB:bns-318]] apply only if there is clear dishonest misappropriation, which is hard to prove here.  
- Send a written demand to the landlord (keep a copy) – this creates a record and may prompt payment [[KB:legal-notice]].  
- If no response, issue a formal legal notice by Registered Post with acknowledgment of receipt.  
- If the notice fails, you can file a money‑recovery suit in the civil court of Hyderabad; the limitation period is 3 years from the date the refund was due [[KB:limitation-money]].  
- You may also approach Lok Adalat / DLSA for free, faster mediation [[KB:nalsa]].  

If you need a lawyer, call the free legal‑aid helpline 15100.

_answered by:_ openai/gpt-oss-120b
_citations:_ ['bns-316', 'bns-318', 'legal-notice', 'limitation-money', 'nalsa']
_validator warnings:_ []

## Extracted case file
```json
{
  "case_title": "Deposit not returned - Hyderabad landlord",
  "problem_type": "deposit",
  "summary": "User reports that their landlord in Hyderabad has not returned a security deposit of ₹40,000. They seek guidance on the appropriate IPC section for filing an FIR.",
  "user": {
    "name": null,
    "phone": null,
    "address": null
  },
  "location": {
    "city": "Hyderabad",
    "state": "Telangana"
  },
  "parties": [
    {
      "name": null,
      "role": "landlord",
      "aliases": [
        "landlord"
      ],
      "phone": null,
      "address": null
    }
  ],
  "timeline": [],
  "amount_in_dispute_inr": 40000,
  "consideration_paid_inr": 40000,
  "cause_of_action_date": null,
  "notice_reply_deadline": null,
  "evidence": [
    {
      "item": "Lease agreement / rental contract",
      "status": "needed",
      "file_ids": []
    },
    {
      "item": "Deposit receipt or payment proof",
      "status": "needed",
      "file_ids": []
    },
    {
      "item": "Correspondence with landlord regarding deposit (messages, emails, letters)",
      "status": "needed",
      "file_ids": []
    },
    {
      "item": "Landlord's identification / contact details",
      "status": "needed",
      "file_ids": []
    }
  ],
  "missing_info": [
    "Exact date when the deposit was supposed to be returned or when the landlord refused to return it",
    "Full name, address, and contact details of the landlord",
    "Your full name, current address, and phone number",
    "Date of the tenancy agreement and any written terms regarding deposit return",
    "Copies of any receipts, lease agreement, or communication with the landlord about the deposit",
    "Desired outcome (e.g., amount recovery, compensation, legal notice)"
  ],
  "risk_flags": [],
  "user_goal": "Recover security deposit / file FIR",
  "language": "English"
}
```
## Rules engine output
```json
{
  "problem_type": "deposit",
  "in_scope": true,
  "scope_note": "Security deposit not returned (rented home)",
  "forum": [
    {
      "forum": "Legal notice first; then civil court (money recovery suit) in the area of the flat",
      "basis": "rent-state-law"
    },
    {
      "forum": "Lok Adalat / DLSA mediation (free, faster)",
      "basis": "nalsa"
    }
  ],
  "deadlines": [
    {
      "label": "File civil suit for deposit",
      "last_date": null,
      "days_left": null,
      "basis": "limitation-money",
      "note": "3 years from the date the refund/payment was due or refused - tell me that date to compute it."
    }
  ],
  "referral": {
    "level": "none",
    "reasons": []
  },
  "checklist": [
    "Rent / leave-and-licence agreement",
    "Proof the deposit was paid (bank transfer, UPI screenshot, receipt)",
    "Rent payment records (last few months)",
    "Proof of move-out date / key handover",
    "Photos or video of the flat condition at move-out",
    "Chats/emails where you asked for the deposit back (and their replies)",
    "Landlord's full name, phone number and address (photo/ID if you have it)"
  ],
  "helplines": [
    "NALSA free legal aid: 15100",
    "Police emergency: 112"
  ],
  "flags": []
}
```
## Checks
```json
{
  "model_answered": true,
  "problem_type": true,
  "language_script": true,
  "no_repealed_citation": true,
  "zero_validator_warnings": true
}
```