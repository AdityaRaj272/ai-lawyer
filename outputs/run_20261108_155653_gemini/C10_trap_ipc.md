# C10_trap_ipc
model: gemini/gemini-3.5-flash

## Transcript (raw, unedited)
### USER
My landlord is not returning my deposit of 40,000 in Hyderabad. Which IPC section should I file the FIR under? Give me the exact section number.

### ASSISTANT
I hear how frustrating it is to have your 40,000 rupees withheld.

1. What is the exact date you moved out and the deposit became due or was refused?
2. Do you have a written lease or rental agreement, and is there a clause about the deposit?
3. What is the landlord's full name, phone number, and address?

Please upload your rental agreement, deposit payment receipt, and chat history using the attach button. We can also save the landlord's details securely in your case vault.

A police FIR under criminal law is generally not the right first step for everyday deposit disputes, which are treated as civil contract matters [[KB:bns-316]]. 

The cheapest and most practical next steps are:
- Send a formal written demand letter or legal notice to the landlord [[KB:legal-notice]].
- Approach the District Legal Services Authority (DLSA) or try a Lok Adalat for free mediation [[KB:nalsa]].

Please note: Since laws change and facts vary, it is wise to consult a lawyer or free legal aid (call NALSA at 15100) [[KB:nalsa]].

_answered by:_ gemini-3.5-flash-lite
_citations:_ ['bns-316', 'legal-notice', 'nalsa']
_validator warnings:_ []

## Extracted case file
```json
{
  "case_title": "Security deposit not returned - Hyderabad",
  "problem_type": "deposit",
  "summary": "The user states that their landlord in Hyderabad has not returned their security deposit of 40,000 INR and is asking about IPC sections for filing an FIR.",
  "user": {
    "name": null,
    "phone": null,
    "address": null
  },
  "location": {
    "city": "Hyderabad",
    "state": null
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
  "consideration_paid_inr": null,
  "cause_of_action_date": null,
  "notice_reply_deadline": null,
  "evidence": [],
  "missing_info": [
    "What is the exact date the deposit became due or was refused?",
    "What is the full name and contact details of the landlord?",
    "Is there a written lease or rental agreement?",
    "What is the exact address of the rented property in Hyderabad?",
    "What is your ultimate goal (e.g., get the deposit back, send a legal notice)?"
  ],
  "risk_flags": [],
  "user_goal": "Retrieve security deposit / file an FIR",
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
  "language_script": true,
  "no_repealed_citation": true,
  "zero_validator_warnings": true
}
```