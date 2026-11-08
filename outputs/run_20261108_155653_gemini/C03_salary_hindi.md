# C03_salary_hindi
model: gemini/gemini-3.5-flash

## Transcript (raw, unedited)
### USER
मैंने सितंबर में नौकरी छोड़ दी थी लेकिन कंपनी ने मेरी आखिरी दो महीने की सैलरी अभी तक नहीं दी है। HR फोन नहीं उठाता। मैं दिल्ली में काम करता था।

### ASSISTANT
मैं समझ सकता हूँ कि सैलरी न मिलने और एचआर द्वारा फोन न उठाने से आपको कितनी परेशानी हो रही होगी।

1. कंपनी का पूरा नाम और आधिकारिक पता क्या है?
2. पिछले दो महीनों की बकाया सैलरी की कुल रकम कितनी है?
3. आपने सितंबर में किस तारीख को नौकरी छोड़ी थी?

कृपया अपने एप्लॉयमेंट एग्रीमेंट, सैलरी स्लिप्स, या सैलरी मिलने वाले बैंक स्टेटमेंट की तस्वीरें यहाँ अटैच बटन से अपलोड कर दें।

नियम के अनुसार, इस्तीफा देने या नौकरी छूटने के 2 काम के दिन के भीतर बकाया सैलरी मिल जानी चाहिए[[KB:cow-17]]. आप अपने राज्य के श्रम विभाग (लेबर डिपार्टमेंट) या मजदूरी प्राधिकरण के पास तीन साल के भीतर बकाया वेतन के लिए दावा कर सकते हैं[[KB:cow-45]]. सबसे पहले, कंपनी को लिखित में मांग पत्र भेजें और चाहें तो दस्तावेजों के साथ लेबर ऑफिसर के पास शिकायत दर्ज कराएं[[KB:cow-45]].

_answered by:_ gemini-flash-lite-latest
_citations:_ ['cow-17', 'cow-45']
_validator warnings:_ []

## Extracted case file
```json
{
  "case_title": "Unpaid salary - Delhi company",
  "problem_type": "salary",
  "summary": "The user left their job in September and the company has not paid their last two months' salary. The HR manager is ignoring phone calls, and the employment took place in Delhi.",
  "user": {
    "name": null,
    "phone": null,
    "address": null
  },
  "location": {
    "city": "Delhi",
    "state": null
  },
  "parties": [
    {
      "role": "HR manager",
      "name": null,
      "aliases": [
        "HR"
      ],
      "phone": null,
      "address": null
    },
    {
      "role": "company",
      "name": null,
      "aliases": [
        "कंपनी"
      ],
      "phone": null,
      "address": null
    }
  ],
  "timeline": [
    {
      "date": "approx: 2024-09",
      "event": "User left the job",
      "source": "user"
    }
  ],
  "amount_in_dispute_inr": null,
  "consideration_paid_inr": null,
  "cause_of_action_date": null,
  "notice_reply_deadline": null,
  "evidence": [
    {
      "item": "Employment agreement or offer letter",
      "status": "needed",
      "file_ids": []
    },
    {
      "item": "Salary slips for the last two months",
      "status": "needed",
      "file_ids": []
    },
    {
      "item": "Bank statement showing salary credits",
      "status": "needed",
      "file_ids": []
    }
  ],
  "missing_info": [
    "What is the exact company name and official address?",
    "What is the exact amount of unpaid salary for the last two months?",
    "What was the exact date in September when you left the job?",
    "Do you have a written employment contract or offer letter?",
    "What is your full name and contact number?"
  ],
  "risk_flags": [],
  "user_goal": "Recover unpaid salary for the last two months",
  "language": "Hindi (Devanagari)"
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
  "asks_question": true,
  "zero_validator_warnings": true
}
```