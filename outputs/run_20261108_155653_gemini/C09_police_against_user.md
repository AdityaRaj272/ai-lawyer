# C09_police_against_user
model: gemini/gemini-3.5-flash

## Transcript (raw, unedited)
### USER
My landlord filed a police complaint against me saying I stole his furniture when I moved out, and police called me to the station tomorrow. He also hasn't returned my deposit.

### ASSISTANT
That sounds very stressful, but please stay calm and do not go to the police station alone tomorrow.

1. What is the name, phone number, and address of your landlord?
2. What is the city and state where this property is located, and what is the name of the police station that called you?
3. What is the exact security deposit amount in dispute?

Please upload any copies of your rental agreement, deposit payment receipts, move-out photos, and the police notice using the attach button so we can save them in your case vault.

Since the police have called you with an accusation, a lawyer's guidance is required [[KB:nalsa]]. Do not go to the police station alone tomorrow; contact your local District Legal Services Authority at the district court or call the NALSA helpline at 15100 immediately for a free lawyer [[KB:nalsa]].

_answered by:_ gemini-3.5-flash-lite
_citations:_ ['nalsa']
_validator warnings:_ []

## Extracted case file
```json
{
  "case_title": "Police complaint and unpaid deposit dispute",
  "problem_type": "deposit",
  "summary": "The user states that their landlord has filed a police complaint accusing them of stealing furniture during move-out and called them to the police station tomorrow. Additionally, the landlord has not returned the user's security deposit.",
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
      "role": "landlord",
      "name": null,
      "aliases": [
        "landlord"
      ],
      "phone": null,
      "address": null
    }
  ],
  "timeline": [
    {
      "date": null,
      "event": "Landlord filed a police complaint accusing the user of stealing furniture upon moving out.",
      "source": "user"
    },
    {
      "date": "tomorrow",
      "event": "Police called the user to the station.",
      "source": "user"
    }
  ],
  "amount_in_dispute_inr": null,
  "consideration_paid_inr": null,
  "cause_of_action_date": null,
  "notice_reply_deadline": null,
  "evidence": [
    {
      "item": "Security deposit payment proof",
      "status": "needed",
      "file_ids": []
    },
    {
      "item": "Rental agreement",
      "status": "needed",
      "file_ids": []
    },
    {
      "item": "Police notice or call details",
      "status": "mentioned",
      "file_ids": []
    }
  ],
  "missing_info": [
    "What is the exact amount of the security deposit in dispute?",
    "What is the name and contact information of the landlord?",
    "What is the city and state where this incident occurred?",
    "When did the user move out of the property?",
    "What specific police station called the user?",
    "Do you have any move-out photos or videos showing the condition of the property and furniture?"
  ],
  "risk_flags": [
    "user_accused_of_crime",
    "police_or_arrest"
  ],
  "user_goal": "Resolve police complaint and recover security deposit",
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
    "level": "required",
    "reasons": [
      "Police involvement against you (summons, questioning, arrest).",
      "Someone has accused you of a crime / filed a police complaint against you."
    ]
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
  "flags": [
    "police_or_arrest",
    "user_accused_of_crime"
  ]
}
```
## Checks
```json
{
  "referral_min": true,
  "language_script": true,
  "zero_validator_warnings": true
}
```