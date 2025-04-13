import random
import time
import json
from datetime import datetime
import os

# Directory to store data (NEW LOCATION outside /scripts)
DATA_DIR = "../data"  # ⬅️ Go one level up and into 'data'
os.makedirs(DATA_DIR, exist_ok=True)

# Function to generate random vitals based on condition
def generate_vitals(patient_id):
    """
    Generates one record of patient vitals based on condition (normal, abnormal, critical)
    """
    # 80% normal, 10% abnormal, 10% critical
    condition = random.choices(
        ["normal", "abnormal", "critical"], [0.8, 0.1, 0.1]
    )[0]

    # Generate vitals based on condition
    if condition == "normal":
        bp_sys = random.randint(90, 120)  # Reduced upper limit from 130 to 120
        bp_dia = random.randint(60, 80)
        heart_rate = random.randint(60, 95)
        oxygen = random.randint(96, 100)  # Normal oxygen higher
        temperature = round(random.uniform(97, 98.5), 1)

    elif condition == "abnormal":
        bp_sys = random.randint(121, 160)  # Start at 130, extend to 160
        bp_dia = random.randint(81, 95)
        heart_rate = random.randint(96, 110)
        oxygen = random.randint(90, 95)
        temperature = round(random.uniform(99.5, 101), 1)  # Higher than normal temperature

    else:  # critical
        bp_sys = random.randint(161, 190)  # Start higher than abnormal
        bp_dia = random.randint(96, 120)
        heart_rate = random.randint(111, 140)
        oxygen = random.randint(85, 89)
        temperature = round(random.uniform(102, 104), 1)


    vitals = {
        "patient_id": patient_id,
        "heart_rate": heart_rate,
        "bp": f"{bp_sys}/{bp_dia}",
        "oxygen": oxygen,
        "temperature": temperature,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "condition": condition
    }

    return vitals

# Function to simulate vitals data for multiple patients
def simulate_multiple_patients(num_patients=5, records_per_patient=10, interval=0.5):
    """
    Generates vitals data for multiple patients and saves in JSONL format
    """
    print(f"\n📡 Starting Vitals Simulation for {num_patients} patients...\n")
    file_path = os.path.join(DATA_DIR, "vitals_log.jsonl")  # Correct path

    with open(file_path, 'w') as f:
        for pid in range(1, num_patients + 1):
            patient_id = f"P{str(pid).zfill(3)}"  # P001, P002, P003, ...
            print(f"👤 Generating vitals for Patient {patient_id}...")
            for _ in range(records_per_patient):
                vitals = generate_vitals(patient_id)
                print(json.dumps(vitals, indent=2))
                f.write(json.dumps(vitals) + "\n")
                time.sleep(interval)

    print(f"\n✅ Data generation complete. {num_patients * records_per_patient} records saved at → {file_path}\n")

if __name__ == "__main__":
    # You can change numbers as needed
    simulate_multiple_patients(num_patients=5, records_per_patient=10, interval=0.5)
