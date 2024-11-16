from typing import Dict
from datasets import Dataset, DatasetDict, load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer
from transformers.integrations import WandbCallback

data_path = "data"
model_id  = "Qwen2.5-0.5b"


def preprocess_dataset(
    dataset: Dataset
):
    dataset.select_columns(["input", "output", "id"])
    dataset = dataset.map(
        lambda x: {"text": f"{x['input']} {x['response']}"}
    )
    return dataset 

def tokenize(batch:Dict, tokenizer)-> Dict:
    return tokenizer([text + tokenizer.eos_token for text in batch["text"]],
    truncation = True)

def create_dataset(data_path, tokenizer)-> DatasetDict:
    dataset = load_dataset(
        "csv",
        data_files = data_path,
    )

    # Select column
    dataset = preprocess_dataset(dataset)

    # Tokenize dataset
    dataset = dataset.map(
        lambda x: tokenize(x, tokenizer=tokenizer)
        batched=True
    )
    return dataset 

def generate_response(data, model, tokenizer):
    all_responses = []
    for batch in data:
        # Text to tokens
        tokens = tokenizer(batch["input"], truncation=True)
        input_ids_tensor = tokens["input_ids"]
        attention_mask_tensor = tokens["attention_mask"]

        # Generate answers 
        batch_generations_ids = model.generate(
            input_ids_tensor,
            attention_mask_tensor,
            max_new_tokens = 256,
            repetition_penalty = 1.5
        )

        # Decode generated tokens 
        batch_generation = tokenizer.batch_decode(
            batch_generations_ids, skip_special_tokens=True
        )

        all_responses.extend(batch_generation)

    # Final export as txt file
    with open("export_samples.txt", "w") as f:
        for line in all_responses:
            f.write(line + "\n")


def main():

    training_args = {"learning_rate": 1e-5,
                     "num_train_epoch": 1,
                     "per_device_train_batch_size": 4}

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrainer(model_id)

    data_path = "data"
    # 1. Load and preprocess dataset 
    dataset = create_dataset(data_path, tokenizer)

    # 2. Initiate callbacks 
    callbacks = [WandbCallback()]

    # 3. Instantiate Huggingface Trainer for model training
    trainer = Trainer(
        model = model,
        tokenizer = tokenizer,
        args = training_args,
        train_dataset = dataset["train"],
        eval_dataset = dataset["val"],
        callbacks = callbacks
    )

    # 4. Begin training
    trainer.train() 

    # 5. Generate Sample response 
    generate_sample_response(dataset["val"], model, tokenizer)
