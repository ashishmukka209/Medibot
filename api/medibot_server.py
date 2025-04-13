# from fastapi import FastAPI, Depends, HTTPException, status
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# import requests
# import json

# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# import torch

# # ✅ Load fine-tuned model once
# tokenizer = AutoTokenizer.from_pretrained("./finetuned_medibot_model")
# model = AutoModelForSeq2SeqLM.from_pretrained("./finetuned_medibot_model")

# # 🛡️ Secure API
# security = HTTPBearer()
# VALID_TOKEN = "medibot_secret_token_123"

# # 🛡️ Telegram Bot Config
# TELEGRAM_BOT_TOKEN = "*****"    # Your Bot Token
# TELEGRAM_CHAT_ID = "****"            # Your Chat ID
# TELEGRAM_BUTTON_URL = "https://t.me/userName"  # Your hospital or Telegram link

# # 🛡️ Verify incoming token
# def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     if credentials.credentials != VALID_TOKEN:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or missing token 🚫",
#         )

# # 📢 Send Telegram Alert (with Button)
# def send_telegram_alert(patient_id, vitals, status, report):
#     message = f"""
# 🚑 <b>Critical Patient Alert!</b>
# 🆔 <b>Patient ID</b>: {patient_id}
# ❤️ <b>Heart Rate</b>: {vitals['heart_rate']} bpm
# 🫁 <b>Oxygen</b>: {vitals['oxygen']} %
# 🌡️ <b>Temperature</b>: {vitals['temperature']} °F
# 🩸 <b>Blood Pressure</b>: {vitals['bp_sys']}/{vitals['bp_dia']} mmHg
# 🚨 🚨 <b>Status:</b> <b>{status}</b>

# 📝 <b>Medical Report</b>:
# {report}
# """
#     url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
#     payload = {
#         "chat_id": TELEGRAM_CHAT_ID,
#         "text": message,
#         "parse_mode": "HTML",
#         "reply_markup": json.dumps({
#             "inline_keyboard": [
#                 [
#                     {
#                         "text": "✅ Acknowledge Alert",
#                         "url": TELEGRAM_BUTTON_URL
#                     }
#                 ]
#             ]
#         })
#     }
#     try:
#         response = requests.post(url, json=payload)
#         print(response.text)  # Debug print
#         print(f"✅ Telegram alert sent for patient {patient_id}")
#     except Exception as e:
#         print(f"❌ Failed to send Telegram alert: {e}")

# # 🚑 FastAPI App
# app = FastAPI()

# # 🛡️ Allow frontend to access backend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # 🚑 Vitals Input Model
# class Vitals(BaseModel):
#     patient_id: str
#     heart_rate: int
#     oxygen: int
#     temperature: float
#     bp_sys: int
#     bp_dia: int
#     timestamp: str

# # 📝 Generate Medical Report
# def generate_medical_report(vitals):
#     input_text = (
#         f"Heart Rate: {vitals['heart_rate']} bpm; Oxygen: {vitals['oxygen']}%; "
#         f"Temperature: {vitals['temperature']} °F; Blood Pressure: {vitals['bp_sys']}/{vitals['bp_dia']} mmHg"
#     )
#     inputs = tokenizer(input_text, return_tensors="pt")
#     outputs = model.generate(**inputs, max_length=50)
#     diagnosis = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return diagnosis

# # 🌍 Health Check Endpoint
# @app.get("/")
# def read_root():
#     return {"message": "MediBot Local Model is Alive 🚑"}

# # 🌡️ Vitals Receiver Endpoint
# @app.post("/vitals")
# def receive_vitals(
#     vitals: Vitals,
#     credentials: HTTPAuthorizationCredentials = Depends(verify_token),
# ):
#     vitals_data = vitals.dict()

#     print("\n🩺 New Vitals Received:")
#     print(vitals_data)

#     # 🚨 Determine Status
#     status = "Normal"
#     if (
#         vitals.heart_rate > 130
#         or vitals.oxygen < 90
#         or vitals.temperature > 102.0
#         or vitals.bp_sys > 180
#     ):
#         status = "Critical"
#     elif (
#         vitals.heart_rate > 100
#         or vitals.oxygen < 94
#         or vitals.temperature > 99.5
#     ):
#         status = "Abnormal"

#     # 📝 Generate Report
#     report = generate_medical_report(vitals_data)

#     # 🚑 If critical, send Telegram alert
#     if status == "Critical":
#         send_telegram_alert(vitals.patient_id, vitals_data, status, report)

#     return {
#         "patient_id": vitals.patient_id,
#         "timestamp": vitals.timestamp,
#         "status": status,
#         "report": report,
#     }
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
import json

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# ✅ Load the highlighted fine-tuned model
tokenizer = AutoTokenizer.from_pretrained("./highlighted_finetuned_medibot_model")
model = AutoModelForSeq2SeqLM.from_pretrained("./highlighted_finetuned_medibot_model")

# 🛡️ Security
security = HTTPBearer()
VALID_TOKEN = "medibot_secret_token_123"

# 🔔 Telegram Alert Setup
TELEGRAM_BOT_TOKEN = "****"   # 👈 Replace
TELEGRAM_CHAT_ID = "*****"       # 👈 Replace
TELEGRAM_BUTTON_URL = "https://t.me/ash1102"  # 👈 Replace

# 🚑 Initialize FastAPI App
app = FastAPI()

# 🔓 Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚑 Vitals Model
class Vitals(BaseModel):
    patient_id: str
    heart_rate: int
    oxygen: int
    temperature: float
    bp_sys: int
    bp_dia: int
    timestamp: str

# 🔒 Verify Token
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != VALID_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token 🚫",
        )

# 📝 Generate Highlighted Medical Report
def generate_medical_report(vitals):
    input_text = (
        f"Heart Rate: {vitals['heart_rate']} bpm; Oxygen: {vitals['oxygen']}%; "
        f"Temperature: {vitals['temperature']} °F; Blood Pressure: {vitals['bp_sys']}/{vitals['bp_dia']} mmHg"
    )
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=128)
    diagnosis = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return diagnosis

# 📢 Telegram Alert
def send_telegram_alert(patient_id, vitals, status, report):
    message = f"""
🚑 <b>Critical Patient Alert!</b>
🆔 <b>Patient ID</b>: {patient_id}
❤️ <b>Heart Rate</b>: {vitals['heart_rate']} bpm
🫁 <b>Oxygen</b>: {vitals['oxygen']} %
🌡️ <b>Temperature</b>: {vitals['temperature']} °F
🩸 <b>Blood Pressure</b>: {vitals['bp_sys']}/{vitals['bp_dia']} mmHg
🚨 <b>Status</b>: <b>{status}</b>

📝 <b>Medical Report</b>:
{report}
"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "reply_markup": json.dumps({
            "inline_keyboard": [
                [{"text": "✅ Acknowledge", "url": TELEGRAM_BUTTON_URL}]
            ]
        })
    }
    try:
        requests.post(url, json=payload)
        print(f"✅ Telegram alert sent for patient {patient_id}")
    except Exception as e:
        print(f"❌ Failed to send Telegram alert: {e}")

# 🌍 Health Check
@app.get("/")
def read_root():
    return {"message": "MediBot Local Model is Alive 🚑"}

# 🌡️ Vitals Endpoint
@app.post("/vitals")
def receive_vitals(vitals: Vitals, credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    vitals_data = vitals.dict()

    print("\n🩺 New Vitals Received:")
    print(vitals_data)

    status = "Normal"
    if vitals.heart_rate > 130 or vitals.oxygen < 90 or vitals.temperature > 102.0 or vitals.bp_sys > 180:
        status = "Critical"
    elif vitals.heart_rate > 100 or vitals.oxygen < 94 or vitals.temperature > 99.5:
        status = "Abnormal"

    report = generate_medical_report(vitals_data)

    if status == "Critical":
        send_telegram_alert(vitals.patient_id, vitals_data, status, report)

    return {
        "patient_id": vitals.patient_id,
        "timestamp": vitals.timestamp,
        "status": status,
        "report": report,
    }
