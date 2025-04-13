# notebooks/alert_agent.py

def send_alert(vitals, status):
    """
    Simulates sending an alert if the patient is critical.
    """
    if status == "Critical":
        print("\n🚨 EMERGENCY ALERT!")
        print(f"Patient {vitals['patient_id']} vitals are critical at {vitals['timestamp']}. Immediate action required.\n")
