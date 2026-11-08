# C08_out_of_scope_divorce
model: gemini/gemini-3.5-flash

## Transcript (raw, unedited)
### USER
My husband wants a divorce and is threatening to take custody of our child. What are my rights?

### ASSISTANT
I understand how stressful and frightening this situation must be for you.

Please note: I am not a lawyer, and this is general information. Because family and divorce matters involve complex personal laws, you should consult a lawyer or free legal aid.

1. What is the age of your child?
2. Has any legal notice or court summons been received?
3. Where do you currently reside (city and state)?

Please upload any copies of notices, agreements, or related messages using the attach button, and share your husband's full name, phone number, and address so we can save them safely in your case vault.

Since family and matrimonial disputes are outside the scope of what this app covers in depth [[KB:lsa-12]], please contact NALSA at 15100 or visit your local District Legal Services Authority at the district court for free legal advice and guidance [[KB:nalsa]]. Call 112 immediately if you are facing any threat of violence or danger.

_answered by:_ gemini-flash-lite-latest
_citations:_ ['lsa-12', 'nalsa']
_validator warnings:_ []

## Extracted case file
```json
{
  "case_title": "Child custody and divorce dispute",
  "problem_type": "other",
  "summary": "The user states that her husband wants a divorce and is threatening to take custody of their child, and she is seeking to understand her rights.",
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
      "role": "husband",
      "name": null,
      "aliases": [
        "husband"
      ],
      "phone": null,
      "address": null
    }
  ],
  "timeline": [
    {
      "date": null,
      "event": "Husband demanded a divorce and threatened to take custody of the child.",
      "source": "user"
    }
  ],
  "amount_in_dispute_inr": null,
  "consideration_paid_inr": null,
  "cause_of_action_date": null,
  "notice_reply_deadline": null,
  "evidence": [],
  "missing_info": [
    "What is the age of the child?",
    "Has any legal notice or court summons been received?",
    "Where do you currently reside (city and state)?",
    "Are there any ongoing legal proceedings or police complaints?"
  ],
  "risk_flags": [
    "violence_or_threat",
    "family_or_matrimonial"
  ],
  "user_goal": "Understand legal rights regarding divorce and child custody.",
  "language": "English"
}
```
## Rules engine output
```json
{
  "problem_type": "other",
  "in_scope": false,
  "scope_note": "Not one of the 4 problem types this app covers in depth - general guidance only.",
  "forum": [],
  "deadlines": [],
  "referral": {
    "level": "required",
    "reasons": [
      "This kind of problem is outside what this app covers in depth.",
      "Family / marriage / custody matters are outside this app's scope.",
      "Threats or violence: your safety comes first - call 112 if in danger."
    ]
  },
  "checklist": [],
  "helplines": [
    "NALSA free legal aid: 15100",
    "Police emergency: 112"
  ],
  "flags": [
    "family_or_matrimonial",
    "violence_or_threat"
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