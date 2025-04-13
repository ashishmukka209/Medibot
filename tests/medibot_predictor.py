# medibot_predictor.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# 1. Load your fine-tuned model
tokenizer = AutoTokenizer.from_pretrained("./finetuned_medibot_model")
model = AutoModelForSeq2SeqLM.from_pretrained("./finetuned_medibot_model")

# 2. Function to generate medical report
def generate_diagnosis(input_vitals):
    inputs = tokenizer(input_vitals, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=50)
    report = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return report

# 3. Example usage
if __name__ == "__main__":
    vitals = "Heart Rate: 138 bpm; Oxygen: 84%; Temperature: 103.5 °F; Blood Pressure: 185/115 mmHg"
    diagnosis = generate_diagnosis(vitals)
    print("\n🩺 Patient Diagnosis:")
    print(diagnosis)
