"""Generate synthetic evidence files (fictional people/companies) for demos and the retrieval eval.

python samples/make_samples.py   ->  samples/evidence/*
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import docx
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "evidence"
OUT.mkdir(parents=True, exist_ok=True)


def font(size):
    for name in ("arial.ttf", "DejaVuSans.ttf", "Arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def whatsapp(path, contact, msgs, date_label):
    W, H = 720, 160 + 120 * len(msgs)
    im = Image.new("RGB", (W, H), "#ece5dd")
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 90], fill="#075e54")
    d.text((90, 22), contact, fill="white", font=font(30))
    d.text((90, 58), "online", fill="#cfe9e5", font=font(20))
    d.ellipse([20, 18, 75, 73], fill="#cccccc")
    d.text((W // 2 - 60, 105), date_label, fill="#555", font=font(20))
    y = 145
    for who, text, t in msgs:
        mine = who == "me"
        lines = [text[i:i + 38] for i in range(0, len(text), 38)]
        h = 30 * len(lines) + 40
        x0 = W - 470 if mine else 20
        d.rounded_rectangle([x0, y, x0 + 450, y + h], 14, fill="#dcf8c6" if mine else "white")
        for i, ln in enumerate(lines):
            d.text((x0 + 15, y + 10 + 30 * i), ln, fill="black", font=font(24))
        d.text((x0 + 370, y + h - 28), t, fill="#777", font=font(18))
        y += h + 20
    im.crop((0, 0, W, y + 10)).save(path)


def card(path, lines, bg="#ffffff", size=(640, 380)):
    im = Image.new("RGB", size, bg)
    d = ImageDraw.Draw(im)
    y = 25
    for text, sz, col in lines:
        d.text((30, y), text, fill=col, font=font(sz))
        y += sz + 18
    im.save(path)


# --- salary case (Priya vs BrightPath Solutions) ---
whatsapp(OUT / "IMG_20260903_whatsapp.png", "Rohit Mehra HR", [
    ("me", "Hi Rohit, my September salary of Rs 45,000 is still pending. When will it be credited?", "10:02"),
    ("them", "Company is in losses. Don't expect anything this month.", "10:15"),
    ("me", "It's been 3 weeks after my last day. I need my salary and relieving letter please.", "10:16"),
    ("them", "Stop messaging me again and again. Just f*** off.", "10:20"),
], "3 October 2026")

card(OUT / "IMG_20260712_id.jpg", [
    ("BrightPath Solutions Pvt. Ltd.", 30, "#0b3d91"), ("EMPLOYEE IDENTITY CARD", 22, "#444"),
    ("Name: Rohit Mehra", 28, "black"), ("Designation: HR Manager", 26, "black"),
    ("Emp ID: BPS-0193   Blood group: B+", 22, "black"), ("Phone: +91 98200 11223", 22, "black"),
    ("Office: 4th floor, Orion Tower, Andheri East, Mumbai", 18, "#333")], bg="#eef3ff")

card(OUT / "payslip_aug_2026.png", [
    ("BrightPath Solutions Pvt. Ltd. - PAYSLIP", 26, "#0b3d91"), ("Month: August 2026", 22, "black"),
    ("Employee: Priya Sharma   Emp ID: BPS-0457", 22, "black"), ("Designation: Customer Support Executive", 20, "black"),
    ("Gross salary: Rs 45,000   Deductions: Rs 1,800", 22, "black"), ("Net pay: Rs 43,200   Credited: 07-09-2026", 22, "black")],
    size=(720, 300))

d = docx.Document()
d.add_heading("BrightPath Solutions Pvt. Ltd. - Appointment Letter", 1)
for p in ["Date: 2 January 2025", "To: Ms. Priya Sharma, Thane, Maharashtra",
          "We are pleased to appoint you as Customer Support Executive at our Andheri East, Mumbai office from 15 January 2025.",
          "Monthly gross salary: Rs 45,000, payable by the 7th of the following month.",
          "Notice period: 30 days from either side. Full and final settlement will be processed within 45 days of the last working day.",
          "For BrightPath Solutions Pvt. Ltd. - Rohit Mehra, HR Manager"]:
    d.add_paragraph(p)
d.save(OUT / "appointment_letter.docx")

# --- deposit case (Aman vs landlord Ramesh Gupta) ---
d = docx.Document()
d.add_heading("Leave and Licence Agreement", 1)
for p in ["This agreement is made on 1 April 2025 at Bengaluru between Mr. Ramesh Gupta (Licensor), owner of Flat 302, Sai Residency, "
          "HSR Layout, Bengaluru 560102, and Mr. Aman Verma (Licensee).",
          "Period: 11 months from 1 April 2025. Monthly licence fee: Rs 22,000.",
          "Security deposit: Rs 1,10,000 (interest free), refundable within 15 days of the Licensee vacating and handing over the keys, "
          "after deducting unpaid dues or damages beyond normal wear and tear.",
          "Either party may terminate with one month's written notice.",
          "Signed: Ramesh Gupta (Licensor)   Aman Verma (Licensee)"]:
    d.add_paragraph(p)
d.save(OUT / "rent_agreement_flat302.docx")

card(OUT / "Screenshot_upi_payment.png", [
    ("Payment successful", 30, "#1a7f37"), ("Rs 1,10,000", 44, "black"),
    ("Paid to: RAMESH GUPTA", 24, "black"), ("UPI ID: rameshg@okhdfc", 22, "#333"),
    ("29 Mar 2025, 6:42 PM", 22, "#333"), ("UPI transaction ID: 508812345678", 20, "#555"),
    ("Note: security deposit flat 302", 20, "#555")], bg="#f4fff6", size=(560, 420))

# --- optional synthetic voice note (Windows SAPI) ---
wav = OUT / "call_recording_hr.wav"
if sys.platform == "win32" and not wav.exists():
    text = ("Hello Priya, this is Rohit from HR. Look, your September salary and settlement will not be paid this month. "
            "Management has put everything on hold. Do not call me again about this.")
    ps = ("Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
          f"$s.SetOutputToWaveFile('{wav}'); $s.Speak('{text}'); $s.Dispose()")
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=False)

print("Wrote:", *sorted(p.name for p in OUT.iterdir()), sep="\n  ")
