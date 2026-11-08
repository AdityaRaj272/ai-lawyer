# C01_deposit_english
model: groq/openai/gpt-oss-120b

## Transcript (raw, unedited)
### USER
My landlord in Bangalore is not returning my security deposit of Rs 1,10,000. I vacated the flat on 31 August 2026 and handed over keys. It's been more than 2 months, he keeps saying he'll pay next week.

### ASSISTANT
I understand you’re still waiting for your ₹1,10,000 deposit.  

1. What is your landlord’s full name, address, and phone number?  
2. Do you have a receipt or bank‑transfer proof showing you paid the deposit?  
3. Can you upload any messages/emails where the landlord promised to return the deposit (including the date of that promise)?

*Please attach the lease agreement, the deposit payment proof, and the communication screenshots using the attach button.*

**Where you stand & next steps (cheapest first):**  
- You have a valid claim for the deposit under your rent agreement and the Model Tenancy Act (if applicable) or state rent law.  
- **Step 1:** Send a written demand (legal notice) to the landlord by Registered Post/Speed Post. State the amount, refer to the lease clause, and give a 7‑day deadline to pay. Keep the receipt and a copy of the notice. [[KB:legal-notice]]  
- **Step 2:** If no payment after the notice, you can approach the **Lok Adalat/DLSA mediation** for a free, faster settlement. [[RULES ENGINE output – forum]]  
- **Step 3:** If still unresolved, file a civil money‑recovery suit in the Bangalore civil court (deadline to file is 30 Sept 2029). [[KB:limitation-money]]  

If you need a free lawyer, call **15100 (NALSA)** or visit your district legal‑services authority.

_answered by:_ openai/gpt-oss-120b
_citations:_ ['legal-notice', 'limitation-money']
_validator warnings:_ []

### USER
His name is Ramesh Gupta. I have the rent agreement and the UPI screenshot of the deposit payment. He hasn't given any reason for not paying.

### ASSISTANT
Got it – you have the agreement and payment proof.  

1. What is your full name, current address, and phone number?  
2. What is Ramesh Gupta’s phone number and residential address?  
3. Do you have any written messages (WhatsApp, email, SMS) where he promised to return the deposit? Please note the exact date of that promise.  

*Please upload the rent agreement, the UPI screenshot, and any communication screenshots using the attach button.*  

**Next practical steps (cheapest first):**  
- **Write a formal demand notice** to Ramesh Gupta (Registered Post/Speed Post, 7‑day payment deadline). You can draft it in the Documents tab; keep the receipt and a copy.  
- **If no response**, approach **Lok Adalat/DLSA mediation** for a free, quicker settlement.  
- **If still unresolved**, file a civil money‑recovery suit in Bangalore before 30 Sept 2029 (Limitation Act).  

If you need free legal aid, call **15100 (NALSA)** or visit your district legal‑services authority.

_answered by:_ openai/gpt-oss-120b
_citations:_ []
_validator warnings:_ []

## Extracted case file
```json
{
  "case_title": "Deposit not returned - Ramesh Gupta, Bangalore",
  "problem_type": "deposit",
  "summary": "User vacated a Bangalore flat on 31 Aug 2026, handed over keys, and paid a security deposit of Rs 110,000. Landlord Ramesh Gupta has not returned the deposit despite promises to pay within a week.",
  "user": {
    "name": null,
    "phone": null,
    "address": null
  },
  "location": {
    "city": "Bangalore",
    "state": "Karnataka"
  },
  "parties": [
    {
      "role": "landlord",
      "aliases": [
        "my landlord"
      ],
      "name": "Ramesh Gupta",
      "phone": null,
      "address": null
    }
  ],
  "timeline": [
    {
      "date": "2026-08-31",
      "event": "Vacated flat and handed over keys to landlord",
      "source": "user"
    },
    {
      "date": "approx: early October 2026",
      "event": "Landlord promised to return deposit next week",
      "source": "user"
    }
  ],
  "amount_in_dispute_inr": 110000,
  "consideration_paid_inr": 110000,
  "cause_of_action_date": "2026-09-30",
  "notice_reply_deadline": null,
  "evidence": [
    {
      "item": "Lease/rent agreement showing security deposit amount",
      "status": "mentioned",
      "file_ids": []
    },
    {
      "item": "UPI screenshot or receipt of deposit payment",
      "status": "mentioned",
      "file_ids": []
    },
    {
      "item": "Written communication (messages/emails) where landlord promised to return deposit",
      "status": "needed",
      "file_ids": []
    },
    {
      "item": "Photograph or video of handover of keys",
      "status": "needed",
      "file_ids": []
    }
  ],
  "missing_info": [
    "Landlord's phone number and address",
    "Your full name, current address, and phone number",
    "Exact date when landlord promised to return the deposit",
    "Upload the rent agreement showing deposit amount",
    "Upload the UPI screenshot or receipt of deposit payment",
    "Any written messages/emails where landlord promised payment"
  ],
  "risk_flags": [],
  "user_goal": "Refund of security deposit of Rs 110,000",
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
      "last_date": "2029-09-30",
      "days_left": 1057,
      "basis": "limitation-money",
      "counted_from": "2026-09-30"
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
  "referral_max": true,
  "language_script": true,
  "asks_upload": true,
  "zero_validator_warnings": true
}
```