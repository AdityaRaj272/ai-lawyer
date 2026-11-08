# C01_deposit_english
model: gemini/gemini-3.5-flash

## Transcript (raw, unedited)
### USER
My landlord in Bangalore is not returning my security deposit of Rs 1,10,000. I vacated the flat on 31 August 2026 and handed over keys. It's been more than 2 months, he keeps saying he'll pay next week.

### ASSISTANT
I hear how frustrating it is to wait over two months for your security deposit of one lakh ten thousand rupees.

1. Please upload your rental agreement, your payment receipt for the deposit, and screenshots of your chat messages with the landlord using the attach button.
2. What is the full name and phone number of your landlord, and the exact address of the rented flat?
3. What is the exact date your rental agreement says the deposit must be returned after moving out, and what excuse is he giving right now?

Since your rental agreement is the main rulebook, keeping the deposit without a valid deduction is a breach of that agreement [[KB:rent-state-law]]. You generally have up to 3 years from when the refund was due to file a civil money-recovery suit [[KB:limitation-money]]. Your first step is to send a formal written demand notice to the landlord [[KB:legal-notice]], which creates a dated record and often pushes them to pay. 

As a reminder: I am an AI legal-help assistant, not a lawyer.

_answered by:_ gemini-3.5-flash-lite
_citations:_ ['rent-state-law', 'limitation-money', 'legal-notice']
_validator warnings:_ []

### USER
His name is Ramesh Gupta. I have the rent agreement and the UPI screenshot of the deposit payment. He hasn't given any reason for not paying.

### ASSISTANT
Thanks for sharing those details about Ramesh Gupta and confirming you have the agreement and payment proof.

1. Please upload your rental agreement, the UPI payment screenshot, and any chat messages using the attach button so they are securely saved in your case vault.
2. What is Ramesh Gupta's phone number and exact address?
3. What is the exact address of the rented flat in Bangalore?

To protect your position, the cheapest and most effective next step is to send a written demand notice to the landlord giving him a final deadline to pay **[1]**. If he still refuses after that notice, you can approach the District Legal Services Authority or Lok Adalat for free mediation **[2]**, or file a civil suit for money recovery **[3]**. You generally have three years from the date the refund was due to take this to a civil court **[4]**.

_answered by:_ gemini-3.5-flash-lite
_citations:_ []
_validator warnings:_ []

## Extracted case file
```json
{
  "case_title": "Security deposit not returned - Ramesh Gupta, Bangalore",
  "problem_type": "deposit",
  "summary": "The user vacated their rented flat in Bangalore on 31 August 2026 and handed over the keys. The landlord, Ramesh Gupta, has failed to return the security deposit of Rs 1,10,000 without providing any specific reason, despite delays of over two months.",
  "user": {
    "name": null,
    "phone": null,
    "address": null
  },
  "location": {
    "city": "Bangalore",
    "state": null
  },
  "parties": [
    {
      "role": "landlord",
      "name": "Ramesh Gupta",
      "aliases": [
        "landlord",
        "he",
        "Ramesh Gupta"
      ],
      "phone": null,
      "address": null
    }
  ],
  "timeline": [
    {
      "date": "2026-08-31",
      "event": "Vacated the flat and handed over keys to the landlord",
      "source": "user"
    }
  ],
  "amount_in_dispute_inr": 110000,
  "consideration_paid_inr": null,
  "cause_of_action_date": "approx: early September 2026",
  "notice_reply_deadline": null,
  "evidence": [
    {
      "item": "Rental agreement",
      "status": "mentioned",
      "file_ids": []
    },
    {
      "item": "Proof of security deposit payment (UPI screenshot)",
      "status": "mentioned",
      "file_ids": []
    },
    {
      "item": "Chat messages or call logs with landlord regarding the deposit",
      "status": "mentioned",
      "file_ids": []
    }
  ],
  "missing_info": [
    "What is the phone number and exact address of the landlord, Ramesh Gupta?",
    "What is the exact address of the rented property?",
    "What is the exact date when the deposit was supposed to be returned according to the rental agreement?",
    "Can you upload the rental agreement, UPI payment screenshot, and chat screenshots?"
  ],
  "risk_flags": [],
  "user_goal": "Get the security deposit refunded",
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
  "problem_type": true,
  "referral_max": true,
  "language_script": true,
  "asks_upload": true,
  "zero_validator_warnings": true
}
```