from typing import Dict, List

from llama_cpp import Llama

from src.utils.constant import CHAT_PROMPT_TEMPLATE


class ChatService:
    def __init__(self, generation_model: Llama):
        self._generation_model = generation_model

    def answer(self, question: str, messages: List[Dict[str, str]]) -> str:
        combined_messages = self._combine_messages(question, messages)
        chat_prompt = CHAT_PROMPT_TEMPLATE.format(
            messages=combined_messages, question=question
        )
        return self._generate(chat_prompt)

    def _combine_messages(self, question: str, messages: List[Dict[str, str]]) -> str:
        message_text = ""
        for message in messages:
            message_text += (
                f"<|im_start|>{message['role']}\n{message['content']}<|im_end|>\n"
            )
        message_text += f"<|im_start|>user\n{question}<|im_end|>\n"
        return message_text

    def _generate(self, prompt: str) -> str:
        response = self._generation_model(
            prompt=prompt,
            temperature=0.2,
            repeat_penalty=1.2,
            max_tokens=2048,
            stop=[
                "\nuser",
                "user: ",
                "user\n",
                "\nTalimatlar",
                "\nMesajlar",
                "\n=====",
                "<|im_end|>",
                "</|im_end",
                "\n<|im_start|>",
                "<|im_start",
            ],
        )
        generated_response: str = response["choices"][0]["text"]
        return generated_response
