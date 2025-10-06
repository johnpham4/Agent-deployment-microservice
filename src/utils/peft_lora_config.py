from typing import Optional, Dict

from pydantic import BaseModel


class Peft_Config(BaseModel):
    # Model identifiers
    model_name: str = "VietAI/vit5-base"
    model_name_finetuned: str = "VietAI/vit5-law-base"

    # LoRA hyperparameters
    lora_r: int = 64
    lora_alpha: int = 16
    lora_dropout: float = 0.1

    # Quantization / precision
    use_4bit: bool = True
    bnb_4bit_compute_dtype: str = "float16"
    bnb_4bit_quant_type: str = "nf4"
    use_nested_quant: bool = False


    # IO / output
    output_dir: str = "./results"

    # Training schedule
    num_train_epochs: int = 1
    max_steps: int = -1
    warmup_ratio: float = 0.03

    # Mixed precision
    fp16: bool = False
    bf16: bool = False

    # Batch sizes
    per_device_train_batch_size: int = 2
    per_device_eval_batch_size: int = 1
    gradient_accumulation_steps: int = 1

    # Memory / optimization
    gradient_checkpointing: bool = True
    max_grad_norm: float = 0.3

    # Optimizer / LR
    learning_rate: float = 2e-5
    weight_decay: float = 0.001
    optim: str = "paged_adamw_32bit"
    lr_scheduler_type: str = "constant"

    # Data handling
    group_by_length: bool = True
    packing: bool = False
    max_seq_length: Optional[int] = None

    # Logging / checkpointing
    save_steps: int = 5000
    logging_steps: int = 50

    # Device mapping (None -> let accelerate/transformers decide, or provide mapping)
    device_map: Optional[Dict[str, int]] = None