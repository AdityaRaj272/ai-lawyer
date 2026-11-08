# C12_tamil_salary
model: gemini/gemini-3.5-flash

## Transcript (raw, unedited)
### USER
என் நிறுவனம் கடந்த இரண்டு மாதங்களாக சம்பளம் கொடுக்கவில்லை. நான் சென்னையில் வேலை செய்கிறேன். என்ன செய்ய வேண்டும்?

### ASSISTANT
உங்கள் நிறுவனத்தில் கடந்த இரண்டு மாதங்களாக சம்பளம் வழங்கப்படவில்லை என்பதைப் புரிந்துகொண்டேன்.

- உங்கள் நிறுவனத்தின் பெயர் மற்றும் முழு முகவரியை என்னிடம் தெரிவிக்க முடியுமா?
- மாதச் சம்பளம் எவ்வளவு மற்றும் எந்தெந்த மாதங்களுக்கான சம்பளம் நிலுவையில் உள்ளது?
- உங்களிடம் பணி நியமன ஆணை (Appointment letter) அல்லது சம்பள ரசீதுகள் (Payslips) உள்ளதா?

உங்கள் சேமிப்பறையில் (Case Vault) பாதுகாப்பாக சேமிக்க, உங்களின் பணி நியமன ஆணை, கடைசியாகப் பெற்ற சம்பள ரசீதுகள், மற்றும் நிறுவனம் தர மறுக்கும் அரட்டைப் பதிவுகளை இணை பொத்தானைப் (Attach button) பயன்படுத்தி இங்கு பதிவேற்றம் செய்யுங்கள்.

சம்பளத்தை உரிய காலத்தில் வழங்குவது நிறுவனத்தின் சட்டப்பூர்வ கடமையாகும் [[KB:cow-17]].

- முதற்கட்டமாக, நிறுவனத்தின் மனிதவளத்துறை (HR) அல்லது மேலாளருக்கு எழுத்துப்பூர்வமாக நினைவூட்டல் மின்னஞ்சல் அல்லது கடிதம் அனுப்பவும் [[KB:legal-notice]].
- அதன்பிறகும் தீர்வு கிடைக்கவில்லை என்றால், தமிழ்நாட்டில் உள்ள சம்பந்தப்பட்ட தொழிலாளர் துறை அதிகாரியிடம் (Labour Department) ஊதிய உரிமை கோரி விண்ணப்பிக்கலாம் [[KB:cow-45]].

_answered by:_ gemini-flash-lite-latest
_citations:_ ['cow-17', 'legal-notice', 'cow-45']
_validator warnings:_ []

## Extracted case file
```json
{
  "case_title": "Unpaid salary - Chennai",
  "problem_type": "salary",
  "summary": "The user states that their employer in Chennai has not paid salary for the past two months and is seeking legal guidance.",
  "user": {
    "name": null,
    "phone": null,
    "address": null
  },
  "location": {
    "city": "Chennai",
    "state": "Tamil Nadu"
  },
  "parties": [],
  "timeline": [],
  "amount_in_dispute_inr": null,
  "consideration_paid_inr": null,
  "cause_of_action_date": null,
  "notice_reply_deadline": null,
  "evidence": [],
  "missing_info": [
    "What is the name of the employer/company?",
    "What is the exact monthly salary amount?",
    "For which specific months is the salary unpaid?",
    "Do you have an employment contract, appointment letter, or payslips?",
    "What is your exact goal (e.g., recover full dues, legal notice)?"
  ],
  "risk_flags": [],
  "user_goal": "Recover unpaid salary",
  "language": "Tamil"
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
  "language_script": true,
  "asks_question": true,
  "zero_validator_warnings": true
}
```