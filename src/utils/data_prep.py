from datasets import load_dataset, concatenate_datasets

def preprocess_function(example):
    SYSTEM_PROMPT = (
    "Bạn là một trợ lý y tế thông minh, trả lời ngắn gọn, chính xác, dựa trên kiến thức y tế Việt Nam."
    )
    user_content = example["question"].strip()
    assistant_content = example["answer"].strip()

    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": assistant_content}
        ]
    }

def get_dataset():
    ds = load_dataset("tarudesu/ViHealthQA")
    full_ds = concatenate_datasets([ds["train"], ds["validation"]])
    full_ds = full_ds.map(preprocess_function, remove_columns=full_ds.column_names).select(range(100))

    return full_ds

def tokenize_and_mask(example, tokenizer, max_length):
    messages = example["messages"]
    prompt_messages = messages[:-1]
    completion = messages[-1]["content"] + tokenizer.eos_token

    # build prompt text using the chat template (no generation content)
    prompt_text = tokenizer.apply_chat_template(prompt_messages, tokenize=False, add_generation_prompt=True)
    full_text = prompt_text + completion

    tokenized_full = tokenizer(full_text, truncation=True, max_length=max_length, padding="max_length")
    tokenized_prompt = tokenizer(prompt_text, truncation=True, max_length=max_length)

    prompt_len = len(tokenized_prompt["input_ids"])
    input_ids = tokenized_full["input_ids"]
    attention_mask = tokenized_full.get("attention_mask", [1]*len(input_ids))

    # labels: -100 for prompt tokens, actual ids for completion tokens
    labels = [-100] * prompt_len + input_ids[prompt_len:]
    if len(labels) < max_length:
        labels = labels + [-100] * (max_length - len(labels))
    else:
        labels = labels[:max_length]

    return {"input_ids": input_ids, "attention_mask": attention_mask, "labels": labels}
