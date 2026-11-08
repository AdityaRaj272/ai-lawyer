# C02_deposit_hinglish_vague
model: gemini/gemini-3.5-flash

## Transcript (raw, unedited)
### USER
bhai mera landlord deposit wapas nahi de raha, 3 mahine ho gaye flat chhode hue. 50 hazaar tha. kya karu?

### ASSISTANT
Yeh toh badi pareshani ki baat hai ki landlord aapka 50,000 rupaye ka deposit roke baitha hai.

1. Kya aap mujhe landlord ka poora naam aur phone number bata sakte hain?
2. Aapne flat kis exact date ya mahine mein chhoda tha?
3. Kya aapke paas written rental agreement hai aur deposit kaise diya tha (UPI/bank transfer)?

Kripya apna rental agreement, deposit payment ka proof, aur landlord ke sath chat history yahan attach button se upload kar dein. Isse aapka case vault strong ho jayega.

Aapka agla kadam yeh hoga ki landlord ko ek formal written demand notice bheji jaye [[KB:legal-notice]]. Agar woh tab bhi na maane, toh hum DLSA ke madhyam se Lok Adalat mein ya civil court mein paisa vasool karne ka case dekh sakte hain [[KB:limitation-money], [[KB:nalsa]].

_answered by:_ gemini-flash-lite-latest
_citations:_ ['legal-notice', 'limitation-money', 'nalsa']
_validator warnings:_ []

## Extracted case file
```json
{
  "case_title": "Security deposit not returned - Landlord",
  "problem_type": "deposit",
  "summary": "The user's landlord has not returned their security deposit of 50,000 rupees even though 3 months have passed since they vacated the flat.",
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
      "name": null,
      "role": "landlord",
      "aliases": [
        "landlord",
        "bhai mera landlord"
      ],
      "phone": null,
      "address": null
    }
  ],
  "timeline": [
    {
      "date": "approx: 3 months ago",
      "event": "User vacated the flat",
      "source": "user"
    }
  ],
  "amount_in_dispute_inr": 50000,
  "consideration_paid_inr": null,
  "cause_of_action_date": null,
  "notice_reply_deadline": null,
  "evidence": [
    {
      "item": "Rental agreement",
      "status": "needed",
      "file_ids": []
    },
    {
      "item": "Proof of deposit payment",
      "status": "needed",
      "file_ids": []
    },
    {
      "item": "Chat history or communications with landlord regarding deposit",
      "status": "needed",
      "file_ids": []
    }
  ],
  "missing_info": [
    "What is the exact date or month when you vacated the flat?",
    "What is the full name and phone number of the landlord?",
    "In which city and state was the rented property located?",
    "Do you have a written rental agreement?",
    "How was the security deposit paid (cash, UPI, bank transfer)?"
  ],
  "risk_flags": [],
  "user_goal": "Get the security deposit back from the landlord",
  "language": "Hinglish (Roman)"
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
  "problem_type": true,
  "referral_max": true,
  "language_script": true,
  "asks_question": true,
  "zero_validator_warnings": true
}
```