# notebooks/vitals_agent.py

def check_vitals(vitals):
    """
    Simple rule-based anomaly detection.
    Returns 'Critical', 'Abnormal', or 'Normal'.
    """
    heart_rate = vitals['heart_rate']
    oxygen = vitals['oxygen']
    temperature = vitals['temperature']
    bp_sys = vitals['bp_sys']
    bp_dia = vitals['bp_dia']

    if (
        heart_rate > 120 or heart_rate < 50 or
        oxygen < 90 or
        temperature > 102 or
        bp_sys > 160 or bp_dia > 100
    ):
        return "Critical"
    
    elif (
        (100 <= heart_rate <= 120) or
        (90 <= oxygen <= 94) or
        (99 <= temperature <= 102) or
        (140 <= bp_sys <= 160) or
        (90 <= bp_dia <= 100)
    ):
        return "Abnormal"
    
    else:
        return "Normal"
