# C08_out_of_scope_divorce
model: groq/openai/gpt-oss-120b

## Transcript (raw, unedited)
### USER
My husband wants a divorce and is threatening to take custody of our child. What are my rights?

### ASSISTANT
I’m sorry to hear you’re dealing with this.  

1. What is the exact date your husband told you he wants a divorce and would take custody?  
2. Please provide your husband’s full name, address, and phone number.  
3. Upload any written proof (messages, emails, letters) of his threat, plus your marriage certificate and your child’s birth certificate.  

**Where you stand & next steps (cheapest first)**  
- You have a right to seek custody; courts decide based on the child’s welfare.  
- Start by collecting all evidence of the threat and any communication about the child’s care.  
- Try an informal settlement or mediation with your husband; a written agreement can be filed later.  
- If settlement fails, you can file a petition for custody in the family court of your district.  
- You may be eligible for free legal aid through NALSA (call 15100) or your local District Legal Services Authority.  

I am not a lawyer.  

If you need a lawyer, contact NALSA at 15100 for free assistance or visit your District Legal Services Authority.

_answered by:_ openai/gpt-oss-120b
_citations:_ []
_validator warnings:_ []

## Extracted case file
```json
{
  "case_title": "Divorce & Custody Rights",
  "problem_type": "other",
  "summary": "User seeks information about her legal rights as her husband wants a divorce and is threatening to take custody of their child. No specific details about dates, names, or location have been provided yet.",
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
      "role": "spouse",
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
      "event": "Husband expressed desire for divorce and threatened to take custody of child",
      "source": "user statement"
    }
  ],
  "amount_in_dispute_inr": null,
  "consideration_paid_inr": null,
  "cause_of_action_date": null,
  "notice_reply_deadline": null,
  "evidence": [
    {
      "item": "Marriage certificate",
      "status": "needed",
      "file_ids": []
    },
    {
      "item": "Child's birth certificate",
      "status": "needed",
      "file_ids": []
    },
    {
      "item": "Written communication (messages/emails) of husband's threat",
      "status": "needed",
      "file_ids": []
    }
  ],
  "missing_info": [
    "Full name of your husband",
    "Husband's address and contact number",
    "Your full name, phone number, and residential address",
    "Exact date when husband communicated his intention to divorce and custody threat",
    "Child's name, date of birth, and current living arrangement",
    "Any written evidence (messages, emails) of the threats"
  ],
  "risk_flags": [
    "family_or_matrimonial"
  ],
  "user_goal": "Understand legal rights regarding divorce and child custody and steps to protect custody",
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
  "model_answered": true,
  "referral_min": true,
  "language_script": true,
  "zero_validator_warnings": true
}
```