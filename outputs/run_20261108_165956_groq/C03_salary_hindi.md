# C03_salary_hindi
model: groq/openai/gpt-oss-120b

## Transcript (raw, unedited)
### USER
मैंने सितंबर में नौकरी छोड़ दी थी लेकिन कंपनी ने मेरी आखिरी दो महीने की सैलरी अभी तक नहीं दी है। HR फोन नहीं उठाता। मैं दिल्ली में काम करता था।

### ASSISTANT
समझ गया, आपने नौकरी छोड़ दी और दो महीने की सैलरी नहीं मिली।  

**कृपया नीचे के प्रश्नों के उत्तर दें और संबंधित दस्तावेज़ अपलोड करें:**  
1. आपका अंतिम कार्य दिवस (तारीख) और इस्तीफ़ा पत्र की तारीख क्या है?  
2. कंपनी का पूरा कानूनी नाम, पत्ता और HR/मैनेजर का नाम व फ़ोन नंबर बताइए।  
3. कुल बकाया वेतन (रुपये में) और आपके पास मौजूद दस्तावेज़ (आफ़र‑लेटर/अपॉइंटमेंट लेटर, सैलरी स्लिप, HR के साथ ई‑मेल/WhatsApp चैट) अपलोड करें।  

**आपकी स्थिति और अगले कदम (सबसे सस्ता पहले):**  
- **वेज़ अथॉरिटी में दावा**: कोड ऑन वेजेज़ 2019 s.45 के तहत आप 3 साल के भीतर राज्य वेज़ अथॉरिटी को आवेदन कर सकते हैं; यह मुफ्त है। [[KB:cow-45]]  
- **लिखित मांग पत्र**: HR को रजिस्टर्ड पोस्ट/स्पीड पोस्ट से लिखित मांग भेजें, रसीद रखें; अक्सर इससे भुगतान हो जाता है। [[KB:legal-notice]]  
- **आगे की कार्रवाई**: यदि कोई जवाब नहीं मिलता, तो कानूनी नोटिस या सिविल कोर्ट में मुकदमा दायर करने पर विचार करें।  

**साक्ष्य**: इलेक्ट्रॉनिक चैट, स्क्रीनशॉट आदि को प्रमाण के रूप में इस्तेमाल किया जा सकता है, बस डिवाइस का प्रमाणपत्र रखें। [[KB:bsa-63]]  

*(मैं वकील नहीं हूँ, लेकिन ऊपर दी गई जानकारी सामान्य मार्गदर्शन के लिए है।)*

_answered by:_ openai/gpt-oss-120b
_citations:_ ['cow-45', 'legal-notice', 'bsa-63']
_validator warnings:_ []

## Extracted case file
```json
{
  "case_title": "Unpaid salary - Delhi employer",
  "problem_type": "salary",
  "summary": "User quit their job in September and has not received the salary for the last two months. HR is unresponsive. The work was based in Delhi.",
  "user": {
    "name": null,
    "phone": null,
    "address": null
  },
  "location": {
    "city": "Delhi",
    "state": "Delhi"
  },
  "parties": [
    {
      "name": null,
      "role": "employer",
      "aliases": [
        "company"
      ],
      "contact": null
    }
  ],
  "timeline": [
    {
      "date": "approx: September 2026",
      "event": "User quit job",
      "source": "user"
    },
    {
      "date": "approx: October 2026",
      "event": "Salary for last two months became due",
      "source": "user"
    }
  ],
  "amount_in_dispute_inr": null,
  "consideration_paid_inr": null,
  "cause_of_action_date": "approx: October 2026",
  "notice_reply_deadline": null,
  "evidence": [
    {
      "item": "salary slips",
      "status": "needed",
      "file_ids": []
    },
    {
      "item": "employment contract or appointment letter",
      "status": "needed",
      "file_ids": []
    },
    {
      "item": "communication with HR (emails, messages)",
      "status": "needed",
      "file_ids": []
    }
  ],
  "missing_info": [
    "Exact last working day (date) and resignation letter date",
    "Employer's legal name and address",
    "Total amount of salary owed (in INR)",
    "Any written agreement or policy regarding salary payment after resignation",
    "Copies of any communication with HR about the pending salary",
    "User's full name and contact details"
  ],
  "risk_flags": [],
  "user_goal": "Receive the pending salary for the last two months",
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
  "model_answered": true,
  "problem_type": true,
  "referral_max": true,
  "language_script": true,
  "asks_question": true,
  "zero_validator_warnings": true
}
```