import os

import requests
from dotenv import load_dotenv

load_dotenv()


class LLM:
    URL = os.getenv(
        "BEE_LLM_URL",
        "http://127.0.0.1:1234/v1/chat/completions",
    )

    MODEL = os.getenv(
        "BEE_MODEL",
        "qwen/qwen2.5-vl-7b",
    )

    def generate(self, messages):
        payload = {
            "model": self.MODEL,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 1024,
        }

        response = requests.post(
            self.URL,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]