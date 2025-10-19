from datasets import load_dataset, concatenate_datasets

def preprocess_function(example):
    user_content = example["question"].strip()
    assistant_content = example["answer"].strip()

    return {
        "messages": [
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": assistant_content}
        ]
    }

def get_dataset():
    ds = load_dataset("tarudesu/ViHealthQA")
    train_ds = concatenate_datasets([ds["train"], ds["validation"]])
    # train_ds = ds["train"]
    train_ds = train_ds.map(preprocess_function, remove_columns=train_ds.column_names)

    val_ds = ds["test"].select(range(200))
    val_ds = val_ds.map(preprocess_function, remove_columns=val_ds.column_names)
    return train_ds, val_ds

def tokenize_and_mask(example, tokenizer, max_length):
    messages = example["messages"]
    prompt_messages = messages[:-1]
    completion = messages[-1]["content"] + tokenizer.eos_token

    prompt_text = tokenizer.apply_chat_template(prompt_messages, tokenize=False, add_generation_prompt=False)
    full_text = prompt_text + completion

    tokenized_full = tokenizer(full_text, truncation=True, max_length=max_length, padding="max_length")
    tokenized_prompt = tokenizer(prompt_text, truncation=True, max_length=max_length)

    prompt_len = len(tokenized_prompt["input_ids"])
    input_ids = tokenized_full["input_ids"]
    attention_mask = tokenized_full.get("attention_mask", [1]*len(input_ids))

    labels = [-100] * prompt_len + input_ids[prompt_len:]
    labels = labels + [-100] * (max_length - len(labels))
    labels = labels[:max_length]

    return {"input_ids": input_ids, "attention_mask": attention_mask, "labels": labels}
