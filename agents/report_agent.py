# notebooks/report_agent.py

import google.generativeai as genai
import re

# (Assumes your Gemini API key is already configured elsewhere)

def markdown_to_text(md_text: str) -> str:
    plain_text = re.sub(r'#+ ', '', md_text)
    plain_text = re.sub(r'\*\*(.*?)\*\*', r'\1', plain_text)
    plain_text = re.sub(r'^\s*[\*\-]\s*', '', plain_text, flags=re.MULTILINE)
    plain_text = re.sub(r'\n\s*\n', '\n\n', plain_text)
    plain_text = plain_text.replace('\\n', '\n')
    return plain_text.strip()

def generate_report(vitals):
    """
    Sends vitals to Gemini and returns a clean medical report.
    """
    prompt = (
        f"Patient ID: {vitals['patient_id']}\n"
        f"Timestamp: {vitals['timestamp']}\n\n"
        f"Heart Rate: {vitals['heart_rate']} bpm\n"
        f"Oxygen Level: {vitals['oxygen']}%\n"
        f"Temperature: {vitals['temperature']} °F\n"
        f"Blood Pressure: {vitals['bp_sys']}/{vitals['bp_dia']} mmHg\n\n"
        f"Generate a short, professional medical report analyzing these vitals.\n"
        f"Highlight if patient is Critical, Abnormal, or Normal.\n"
        f"Format cleanly without markdown symbols."
    )

    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
        response = model.generate_content(prompt)
        raw_report = response.text.strip()
        final_report = markdown_to_text(raw_report)
        return final_report
    
    except Exception as e:
        print("❌ Error in Gemini report generation:", str(e))
        return "⚠️ Error: Unable to generate report at the moment."
