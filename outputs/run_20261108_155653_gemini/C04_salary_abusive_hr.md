# C04_salary_abusive_hr
model: gemini/gemini-3.5-flash

## Transcript (raw, unedited)
### USER
I resigned from BrightPath Solutions in Mumbai, my last day was 10 September 2026. My September salary of 45,000 is not paid. When I asked the HR guy Rohit on WhatsApp he told me to f*** off.

### ASSISTANT
That sounds very frustrating and unprofessional of the HR representative.

1. Please answer these questions so we can get your details saved in your case vault and move forward:
- What is your full name and contact phone number?
- What is the exact address of BrightPath Solutions in Mumbai?
- Do you have a copy of your appointment letter or employment contract?
Please use the attach button to upload your appointment letter, bank statements showing past salary credits, and screenshots of the WhatsApp chat with Rohit.

2. Since you left on 10 September 2026, your final dues must be paid within 2 working days [[KB:cow-17]]. You can file a claim for unpaid wages before the Labour Department / wage authority of your State within 3 years [[KB:cow-45]]. Your next step is to send a formal written demand notice to the company, and we can draft this in the Documents tab once you provide the details.

_answered by:_ gemini-flash-lite-latest
_citations:_ ['cow-17', 'cow-45']
_validator warnings:_ []

### USER
I have the chat screenshot and my appointment letter. What can I do?

### ASSISTANT
That is helpful to have those documents ready.

1. Please upload your chat screenshot and appointment letter using the attach button so they are securely stored in your case vault. Also answer these quick questions:
- What is your full name and contact phone number?
- What is the full address of BrightPath Solutions in Mumbai?
- What is the exact date your final settlement or September salary was promised or due?

2. Monthly wages must be paid before the end of the 7th day of the following month, and dues upon leaving must be cleared within 2 working days [[KB:cow-17]]. You can file a claim for unpaid wages with the Labour Department / wage authority of your State within 3 years [[KB:cow-45]]. Your best next step is to send a written demand notice to the company, which we can draft together in the Documents tab.

_answered by:_ gemini-3.5-flash-lite
_citations:_ ['cow-17', 'cow-45']
_validator warnings:_ []

## Extracted case file
```json
{
  "case_title": "Unpaid salary - BrightPath Solutions, Mumbai",
  "problem_type": "salary",
  "summary": "The user resigned from BrightPath Solutions in Mumbai with their last day on 10 September 2026. The September salary of 45,000 INR remains unpaid, and the HR representative Rohit refused payment via WhatsApp. The user has the WhatsApp chat screenshot and appointment letter.",
  "user": {
    "name": null,
    "phone": null,
    "address": null
  },
  "location": {
    "city": "Mumbai",
    "state": null
  },
  "parties": [
    {
      "role": "employer",
      "name": "BrightPath Solutions",
      "aliases": [
        "BrightPath Solutions"
      ],
      "phone": null,
      "address": null
    },
    {
      "role": "HR manager",
      "name": "Rohit",
      "aliases": [
        "Rohit",
        "the HR guy Rohit"
      ],
      "phone": null,
      "address": null
    }
  ],
  "timeline": [
    {
      "date": "2026-09-10",
      "event": "User's last day at BrightPath Solutions",
      "source": "user"
    },
    {
      "date": null,
      "event": "HR Rohit told the user to f*** off on WhatsApp when asked about the unpaid salary",
      "source": "user"
    }
  ],
  "amount_in_dispute_inr": 45000,
  "consideration_paid_inr": null,
  "cause_of_action_date": null,
  "notice_reply_deadline": null,
  "evidence": [
    {
      "item": "WhatsApp chat screenshot with HR Rohit",
      "status": "mentioned",
      "file_ids": []
    },
    {
      "item": "Appointment letter or employment contract",
      "status": "mentioned",
      "file_ids": []
    },
    {
      "item": "Bank statements showing salary history",
      "status": "needed",
      "file_ids": []
    }
  ],
  "missing_info": [
    "What is the exact date the September salary was due?",
    "What is the user's full name and contact phone number?",
    "What is the full address of BrightPath Solutions?",
    "What specific resolution or outcome does the user want (e.g., full salary, legal notice, formal complaint)?"
  ],
  "risk_flags": [],
  "user_goal": "Recover unpaid September salary of 45,000 INR",
  "language": "English"
}
```
## Rules engine output
```json
{
  "problem_type": "salary",
  "in_scope": true,
  "scope_note": "Unpaid / delayed salary or final settlement",
  "forum": [
    {
      "forum": "Labour Department / wage authority of your State (claim for unpaid wages)",
      "basis": "cow-45"
    },
    {
      "forum": "Legal notice to the employer; civil court for recovery if the wage authority route is not available to you (ask a lawyer)",
      "basis": "legal-notice"
    }
  ],
  "deadlines": [
    {
      "label": "File wage claim",
      "last_date": null,
      "days_left": null,
      "basis": "cow-45",
      "note": "3 years from the date the refund/payment was due or refused - tell me that date to compute it."
    }
  ],
  "referral": {
    "level": "none",
    "reasons": []
  },
  "checklist": [
    "Offer letter / appointment letter",
    "Salary slips (last paid months)",
    "Bank statement showing the last salary credit",
    "Proof you worked in the unpaid period (attendance, emails, work logs)",
    "Resignation / termination / relieving letter",
    "Chats/emails where you asked for your salary (and their replies)",
    "Employer's registered name & address; HR/manager's name, phone (photo/ID card if you have it)"
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