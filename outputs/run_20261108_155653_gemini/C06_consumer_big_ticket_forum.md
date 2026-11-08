# C06_consumer_big_ticket_forum
model: gemini/gemini-3.5-flash

## Transcript (raw, unedited)
### USER
I paid Rs 65 lakh to a builder in Pune for a flat in 2023, possession was promised by March 2025 and it still hasn't been delivered. They don't reply. Which consumer forum do I go to?

### ASSISTANT
That is a frustrating situation to deal with after paying such a large amount.

1. Please tell me:
- What is the exact name of the builder or company?
- Do you have a Builder-Buyer Agreement stating the penalty or refund terms for delayed possession?
- What is your full name and contact number?

Please also use the attach button to upload your Builder-Buyer Agreement and payment receipts here so they are safely stored in your case vault.

Since you paid Rs 65 lakh, which is above Rs 50 lakh and up to Rs 2 crore, the correct forum is the State Consumer Commission ([[KB:cpa-jurisdiction-rules-2021]]). However, before going there, your cheapest first step is to register a grievance on the National Consumer Helpline at 1915 or via consumerhelpline.gov.in, or send a formal written demand notice to the builder [[KB:nch, KB:legal-notice]]. You have time until March 2027 to file a formal consumer complaint [[KB:cpa-69]].

_answered by:_ gemini-flash-lite-latest
_citations:_ ['cpa-jurisdiction-rules-2021', 'cpa-69']
_validator warnings:_ []

## Extracted case file
```json
{
  "case_title": "Delayed flat possession - Builder, Pune",
  "problem_type": "consumer",
  "summary": "The user paid Rs 65 lakh to a builder in Pune in 2023 for a flat promised for possession by March 2025. The builder has failed to deliver the flat by the promised date and is unresponsive.",
  "user": {
    "name": null,
    "phone": null,
    "address": null
  },
  "location": {
    "city": "Pune",
    "state": null
  },
  "parties": [
    {
      "role": "builder",
      "name": null,
      "aliases": [
        "builder"
      ],
      "phone": null,
      "address": null
    }
  ],
  "timeline": [
    {
      "date": "2023",
      "event": "Paid Rs 65 lakh to the builder for a flat",
      "source": "user"
    },
    {
      "date": "2025-03",
      "event": "Promised date of possession",
      "source": "user"
    }
  ],
  "amount_in_dispute_inr": null,
  "consideration_paid_inr": 6500000,
  "cause_of_action_date": "2025-03-01",
  "notice_reply_deadline": null,
  "evidence": [
    {
      "item": "Payment receipt / bank transfer proof",
      "status": "mentioned",
      "file_ids": []
    },
    {
      "item": "Builder-Buyer Agreement / Allotment letter",
      "status": "mentioned",
      "file_ids": []
    }
  ],
  "missing_info": [
    "What is the exact name of the builder / company?",
    "Do you have a Builder-Buyer Agreement stating the penalty or refund terms for delayed possession?",
    "What is your full name and contact number?",
    "Do you want a full refund with interest or possession with compensation?",
    "What is the exact address or project name of the flat in Pune?"
  ],
  "risk_flags": [],
  "user_goal": "Understand which consumer forum to approach and get legal remedy for delayed possession",
  "language": "English"
}
```
## Rules engine output
```json
{
  "problem_type": "consumer",
  "in_scope": true,
  "scope_note": "Refund / defective product / bad service (incl. online)",
  "forum": [
    {
      "forum": "National Consumer Helpline (free, pre-litigation)",
      "basis": "nch"
    },
    {
      "forum": "State Consumer Commission",
      "basis": "cpa-jurisdiction-rules-2021",
      "fee": "Filing fee applies - check the fee table on e-Jagriti",
      "fee_basis": "cpa-fee"
    },
    {
      "forum": "File online at e-jagriti.gov.in",
      "basis": "ejagriti"
    }
  ],
  "deadlines": [
    {
      "label": "File consumer complaint",
      "last_date": "2027-03-01",
      "days_left": 113,
      "basis": "cpa-69",
      "counted_from": "2025-03-01"
    }
  ],
  "referral": {
    "level": "none",
    "reasons": []
  },
  "checklist": [
    "Invoice / order ID / booking confirmation",
    "Payment proof (card/UPI/bank statement)",
    "Photos/video of the defect or problem",
    "Complaint ticket numbers + chats/emails with customer care",
    "Seller / company name and address (from invoice or website)",
    "Warranty card / terms promised at purchase"
  ],
  "helplines": [
    "National Consumer Helpline: 1915",
    "NALSA free legal aid: 15100",
    "Police emergency: 112"
  ],
  "flags": []
}
```
## Checks
```json
{
  "problem_type": true,
  "language_script": true,
  "forum": true,
  "zero_validator_warnings": true
}
```