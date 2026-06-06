# service/llm_service.py

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)


class LLMService:

    def __init__(self):

        self.model_path = "G:\\code_work\\check_cuda\\model\\Qwen3-4B"

        self.model = None
        self.tokenizer = None

    def load_model(self):
        """
        加载模型
        """

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            torch_dtype="auto",
            device_map="auto",
        ).eval()

        self.model.generation_config.max_new_tokens = 2048
        print(self.model.device)
        print("Qwen3-4B 模型加载成功")

    def chat(self, message: str) -> str:
        """
        单轮聊天
        """

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Think briefly and answer directly."
            },
            {
                "role": 'user',
                "content": message,
            },
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt"
        ).to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            # max_new_tokens=512
            max_new_tokens=128,
            do_sample=True,
            temperature=0.7,
        )

        answer = self.tokenizer.decode(
            outputs[0][inputs.input_ids.shape[1]:],
            skip_special_tokens=True
        )

        return answer


llm_service = LLMService()
# llm_service.load_model()
#
# print(
#     llm_service.chat("你好")
# )