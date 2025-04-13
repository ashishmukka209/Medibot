# import pandas as pd
# import torch
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer
# from datasets import Dataset
# from sklearn.model_selection import train_test_split

# # 1. Load Data
# print("📂 Loading dataset...")
# df = pd.read_csv("prepared_training_data.csv")
# print(df.head())

# # 2. Load Model and Tokenizer
# print("🔄 Loading model and tokenizer...")
# model_name = "t5-small"  # Lightweight model
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# # 3. Split into Train and Validation
# train_df, val_df = train_test_split(df, test_size=0.1, random_state=42)
# train_dataset = Dataset.from_pandas(train_df)
# val_dataset = Dataset.from_pandas(val_df)

# # 4. Preprocessing
# print("🛠️ Preparing dataset...")

# def preprocess(example):
#     inputs = tokenizer(example['input_text'], truncation=True, padding="max_length", max_length=256)
#     labels = tokenizer(example['target_text'], truncation=True, padding="max_length", max_length=256)
#     inputs['labels'] = labels['input_ids']
#     return inputs

# # Tokenize
# tokenized_train = train_dataset.map(preprocess, batched=True, remove_columns=train_dataset.column_names)
# tokenized_val = val_dataset.map(preprocess, batched=True, remove_columns=val_dataset.column_names)

# # 5. Training Arguments
# print("⚙️ Setting training arguments...")
# training_args = Seq2SeqTrainingArguments(
#     output_dir="./finetuned_medibot_model",
#     num_train_epochs=5,
#     per_device_train_batch_size=8,
#     per_device_eval_batch_size=8,
#     evaluation_strategy="epoch",
#     save_strategy="epoch",
#     logging_steps=10,
#     save_total_limit=2,
#     predict_with_generate=True,
#     fp16=False,  # Enable this only if you have a good GPU
# )

# # 6. Trainer
# print("🚀 Initializing trainer...")
# trainer = Seq2SeqTrainer(
#     model=model,
#     args=training_args,
#     train_dataset=tokenized_train,
#     eval_dataset=tokenized_val,
# )

# # 7. Train!
# print("🔥 Starting fine-tuning...")
# trainer.train()

# # 8. Save model
# print("💾 Saving model...")
# model.save_pretrained("./finetuned_medibot_model")
# tokenizer.save_pretrained("./finetuned_medibot_model")

# print("✨ Done! Your fine-tuned MediBot model is ready!")

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Trainer
from datasets import Dataset
from sklearn.model_selection import train_test_split

# 1. Load Highlighted Dataset
print("📂 Loading dataset...")
df = pd.read_csv("highlighted_training_data.csv")   # <<== updated file
print(df.head())

# 2. Load Model and Tokenizer
print("🔄 Loading model and tokenizer...")
model_name = "t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# 3. Split into Train and Validation
train_df, val_df = train_test_split(df, test_size=0.1, random_state=42)
train_dataset = Dataset.from_pandas(train_df)
val_dataset = Dataset.from_pandas(val_df)

# 4. Preprocessing
print("🛠️ Preparing dataset...")

def preprocess(example):
    inputs = tokenizer(example['input_text'], truncation=True, padding="max_length", max_length=128)
    labels = tokenizer(example['target_text'], truncation=True, padding="max_length", max_length=128)
    inputs['labels'] = labels['input_ids']
    return inputs

tokenized_train = train_dataset.map(preprocess, batched=True)
tokenized_val = val_dataset.map(preprocess, batched=True)

# 5. Training Arguments
print("⚙️ Setting training arguments...")
training_args = Seq2SeqTrainingArguments(
    output_dir="./highlighted_finetuned_medibot_model",
    num_train_epochs=5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_steps=10,
    save_total_limit=2,
    predict_with_generate=True,
    fp16=False,  # ✅ Use False if you don't have strong GPU
)

# 6. Trainer
print("🚀 Initializing trainer...")
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_val,
)

# 7. Train!
print("🔥 Starting fine-tuning...")
trainer.train()

# 8. Save model
print("💾 Saving model...")
model.save_pretrained("./highlighted_finetuned_medibot_model")
tokenizer.save_pretrained("./highlighted_finetuned_medibot_model")

print("✨ Done! Your highlighted fine-tuned MediBot model is ready!")
