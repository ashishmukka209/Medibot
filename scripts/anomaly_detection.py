# Import Libraries
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report

# Load the Vitals Data
file_path = "../data/vitals_log.jsonl"  # Path to your vitals log file
df = pd.read_json(file_path, lines=True)

# Preprocessing: Split BP into systolic and diastolic
df[['bp_sys', 'bp_dia']] = df['bp'].str.split('/', expand=True)
df['bp_sys'] = df['bp_sys'].astype(int)
df['bp_dia'] = df['bp_dia'].astype(int)

# Drop the original 'bp' column
df.drop(columns=['bp'], inplace=True)

# Select features for model training
features = ['heart_rate', 'oxygen', 'temperature', 'bp_sys', 'bp_dia']
X = df[features]

# Initialize and Train the Isolation Forest model
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X)

# Predict anomalies
df['anomaly'] = model.predict(X)

# -----------------------------------------------
# Add Medical Safety Rules (Hard Safety Check)
# -----------------------------------------------
def hard_safety_check(vitals_row):
    bp_sys = vitals_row['bp_sys']
    bp_dia = vitals_row['bp_dia']
    oxygen = vitals_row['oxygen']
    temperature = vitals_row['temperature']
    
    # Stricter medical thresholds
    if bp_sys >= 130 or bp_dia >= 85:   # BP very slightly abnormal
        return -1
    if oxygen < 94:                     # Oxygen < 94 instead of 92
        return -1
    if temperature >= 100.0:             # Fever slightly stricter
        return -1
    return vitals_row['anomaly']

# Apply the hard safety check
df['anomaly_safe'] = df.apply(hard_safety_check, axis=1)

# -----------------------------------------------
# Evaluation
# -----------------------------------------------

# Map 'condition' to true labels
# normal -> 1, abnormal/critical -> -1
def map_condition_to_label(cond):
    if cond == 'normal':
        return 1
    else:
        return -1

# Create true labels
true_labels = df['condition'].apply(map_condition_to_label)

# Print Final Vitals + Safe Anomaly Predictions
print("\n✅ Final Vitals with Patient ID and Safe Anomaly Prediction:\n")
print(df[['patient_id', 'heart_rate', 'oxygen', 'temperature', 'bp_sys', 'bp_dia', 'condition', 'anomaly_safe']])

# Evaluate Model Performance (after Safety Rules)
print("\n✅ Model Evaluation Report (After Safety Rules):\n")
print(classification_report(true_labels, df['anomaly_safe']))
