from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig, pipeline
import torch
import logging
import time
from typing import Optional
from core.config import settings
import torch
import logging

logger = logging.getLogger(__name__)

class ChatService:
    """Service for managing the LLM model"""

    def __init__(self):
        self.model: Optional[AutoModelForCausalLM] = None
        self.tokenizer: Optional[AutoTokenizer] = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_loaded = False

    async def load_model(self, model_path: str = None) -> str:

        try:
            if model_path is None:
                model_path = settings.MODEL_PATH

            start_time = time.time()

            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True
            )

            # Move model to device manually
            if torch.cuda.is_available():
                self.model = self.model.to("cuda")
            else:
                self.model = self.model.to("cpu")
            self.model.config.use_cache = False
            self.model.config.pretraining_tp = 1

            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.tokenizer.padding_side = "right"
            self.tokenizer.chat_template = settings.CHAT_TEMPLATE

            try:
                self.pipe = pipeline(
                    "text-generation",
                    model=self.model,
                    tokenizer=self.tokenizer,
                    device_map="auto"
                )

            except Exception as e:
                 raise RuntimeError("Model is not loaded")

            load_time = time.time() - start_time
            logger.info(f"Model loaded successfully in {load_time:.2f} seconds")
            self.model_loaded = True


        except Exception as e:
            logger.error("Error while loading model:", e)
            self.model_loaded = False
            raise

    def is_model_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model_loaded and self.model is not None and self.tokenizer is not None

    def generate_response(
        self,
        user_input: str,
        max_tokens: int = None,
        temperature: float = None,
        top_p: float = None
    ) -> str:
        """Generate response from user input"""

        try:
            messages = [
                {"role": "system", "content": "You are an SQL analyst with 15 years of experience writing complex SQL queries. Consider the following tables with their schemas: Write a SQLite SQL query that would help you answer the following question: Remember always return sql query answer, do not return any extra information or explain or add text. \n"},
                {"role": "user", "content": f"{user_input}"}
            ]
            if hasattr(self.tokenizer, 'apply_chat_template'):
                prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            else:
                raise Exception("not chat template")

            response = self.pipe(
                prompt,
                do_sample=False,
                num_beams=4,
                early_stopping=True,  # Dừng sớm khi tìm ra câu trả lời tốt
                repetition_penalty=1.5,  # Tăng để giảm lặp
                max_new_tokens=max_tokens,
                eos_token_id=self.tokenizer.eos_token_id
            )

            generated_text = response[0]['generated_text']

            # Extract only the assistant's response
            if "assistant" in generated_text:
                response = generated_text.split("assistant")[-1].strip()
            else:
                return generated_text

            return response

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise


    def get_chat_history(self, session_id: str, db, limit: int = 50):
        pass

    def get_analytics(self, db, days: int = 7):
        pass


chatService = ChatService()