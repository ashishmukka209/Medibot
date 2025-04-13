import random
import time
from datetime import datetime
import pandas as pd
from sklearn.ensemble import IsolationForest

# List of features to use in model
features = ['heart_rate', 'oxygen', 'temperature', 'bp_sys', 'bp_dia']

# Function to generate random vitals
def generate_vitals(patient_id):
    condition = random.choices(
        ["normal", "abnormal", "critical"], [0.8, 0.1, 0.1]
    )[0]

    if condition == "normal":
        bp_sys = random.randint(90, 120)
        bp_dia = random.randint(60, 80)
        heart_rate = random.randint(60, 95)
        oxygen = random.randint(96, 100)
        temperature = round(random.uniform(97, 98.5), 1)
    elif condition == "abnormal":
        bp_sys = random.randint(121, 160)
        bp_dia = random.randint(81, 95)
        heart_rate = random.randint(96, 110)
        oxygen = random.randint(90, 95)
        temperature = round(random.uniform(99.5, 101), 1)
    else:  # critical
        bp_sys = random.randint(161, 190)
        bp_dia = random.randint(96, 120)
        heart_rate = random.randint(111, 140)
        oxygen = random.randint(85, 89)
        temperature = round(random.uniform(102, 104), 1)

    vitals = {
        "patient_id": patient_id,
        "heart_rate": heart_rate,
        "temperature": temperature,
        "bp_sys": bp_sys,
        "bp_dia": bp_dia,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "condition": condition  # For checking only
    }
    return vitals

# Hard safety check to catch medically critical cases
def hard_safety_check(vitals_row):
    bp_sys = vitals_row['bp_sys']
    bp_dia = vitals_row['bp_dia']
    oxygen = vitals_row['oxygen']
    temperature = vitals_row['temperature']
    heart_rate = vitals_row['heart_rate']
    
    if bp_sys >= 130 or bp_dia >= 85:
        return -1
    if oxygen < 94:
        return -1
    if temperature >= 100.0:
        return -1
    if heart_rate > 120:
        return -1
    return 1

# Quick training of Isolation Forest model on simulated normal vitals
def train_isolation_forest():
    training_data = []
    for _ in range(100):
        vitals = generate_vitals(patient_id="P000")
        training_data.append([
            vitals['heart_rate'], vitals['oxygen'], vitals['temperature'],
            vitals['bp_sys'], vitals['bp_dia']
        ])
    df_train = pd.DataFrame(training_data, columns=features)
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(df_train)
    return model

if __name__ == "__main__":
    print("\n📡 Starting Real-Time Vitals Streaming...\n")
    
    # Step 1: Train the model
    model = train_isolation_forest()
    
    # Step 2: Start streaming vitals data
    for i in range(10):  # Simulate 10 records (you can increase later)
        patient_id = f"P{str(random.randint(1, 5)).zfill(3)}"
        vitals = generate_vitals(patient_id)
        
        print(f"\nGenerated Vitals for {patient_id} at {vitals['timestamp']}:")
        for key, value in vitals.items():
            if key != "condition":
                print(f"{key}: {value}")
        
        # Step 3: Predict anomaly using Isolation Forest
        X_new = pd.DataFrame([[
            vitals['heart_rate'], vitals['oxygen'], vitals['temperature'],
            vitals['bp_sys'], vitals['bp_dia']
        ]], columns=features)
        
        prediction = model.predict(X_new)[0]  # -1 means anomaly
        
        # Step 4: Apply hard safety check
        final_prediction = hard_safety_check(vitals)
        
        # Step 5: Emergency alert if either model or hard rules detect danger
        if prediction == -1 or final_prediction == -1:
            print("\n🚨 EMERGENCY ALERT! Patient vitals critical!")
            print(vitals)
        
        time.sleep(2)  # Wait 2 seconds before next vitals
        