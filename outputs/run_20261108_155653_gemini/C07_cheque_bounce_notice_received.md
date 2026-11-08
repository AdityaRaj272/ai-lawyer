# C07_cheque_bounce_notice_received
model: gemini/gemini-3.5-flash

## Transcript (raw, unedited)
### USER
I got a legal notice saying a cheque I gave to a friend bounced and I have to pay Rs 2 lakh within 15 days or they will file a case under cheque bounce. I received it yesterday. What does this mean?

### ASSISTANT
It is stressful to receive a cheque bounce notice, but I am here to help you understand it.

1. What is the exact date printed on the legal notice?
2. What is the full name and contact details of the friend who sent the notice?
3. What was the underlying transaction or reason for issuing this cheque?

Please use the attach button to upload the legal notice, the bank memo showing the bounce, and any payment receipts or chats about this money so we can store them safely in your case vault.

Under the law [[KB:ni-138]], a cheque bounce notice gives you a 15-day window from the date you received it to make the payment before a criminal complaint can be filed [[KB:ni-138]]. Because cheque-bounce cases are serious criminal proceedings with strict deadlines, a lawyer is required to handle your response properly. Please call NALSA at 15100 or visit your local District Legal Services Authority to get a free lawyer immediately.

_answered by:_ gemini-flash-lite-latest
_citations:_ ['ni-138']
_validator warnings:_ []

## Extracted case file
```json
{
  "case_title": "Cheque bounce notice - 2 Lakhs",
  "problem_type": "notice_received",
  "summary": "The user received a legal notice yesterday regarding a bounced cheque issued to a friend, demanding payment of Rs 2 lakh within 15 days under threat of legal action.",
  "user": {
    "name": null,
    "phone": null,
    "address": null
  },
  "location": {
    "city": null,
    "state": null
  },
  "parties": [
    {
      "role": "friend",
      "name": null,
      "aliases": [
        "friend"
      ],
      "phone": null,
      "address": null
    }
  ],
  "timeline": [
    {
      "date": "yesterday",
      "event": "Received legal notice regarding bounced cheque demanding Rs 2 lakh within 15 days.",
      "source": "user"
    }
  ],
  "amount_in_dispute_inr": 200000,
  "consideration_paid_inr": null,
  "cause_of_action_date": null,
  "notice_reply_deadline": null,
  "evidence": [
    {
      "item": "Legal notice",
      "status": "mentioned",
      "file_ids": []
    },
    {
      "item": "Copy of the bounced cheque",
      "status": "needed",
      "file_ids": []
    },
    {
      "item": "Bank memo stating reasons for bounce",
      "status": "needed",
      "file_ids": []
    }
  ],
  "missing_info": [
    "What is the exact date the legal notice was received?",
    "What is the exact date printed on the legal notice?",
    "What is the full name and contact details of the friend who sent the notice?",
    "What was the underlying transaction or reason for issuing the cheque to the friend?",
    "Do you have a copy of the legal notice and the bank memo for the bounced cheque?"
  ],
  "risk_flags": [
    "cheque_bounce",
    "court_summons"
  ],
  "user_goal": "Understand what the legal notice means and how to reply to it.",
  "language": "English"
}
```
## Rules engine output
```json
{
  "problem_type": "notice_received",
  "in_scope": true,
  "scope_note": "Understanding & replying to a notice you received",
  "forum": [],
  "deadlines": [],
  "referral": {
    "level": "required",
    "reasons": [
      "Cheque-bounce cases are criminal proceedings with strict deadlines.",
      "You have received court summons / a court case is already filed - court dates are binding."
    ]
  },
  "checklist": [
    "The notice itself (all pages, both sides)",
    "Envelope / courier slip showing the date you received it",
    "The agreement or transaction the notice is about",
    "Your proof for your side (payments, chats, receipts)"
  ],
  "helplines": [
    "NALSA free legal aid: 15100",
    "Police emergency: 112"
  ],
  "flags": [
    "cheque_bounce",
    "court_summons"
  ]
}
```
## Checks
```json
{
  "problem_type": true,
  "referral_min": true,
  "language_script": true,
  "zero_validator_warnings": true
}
```