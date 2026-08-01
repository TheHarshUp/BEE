import requests


class LLM:
    URL = "http://26.225.84.227:1234/v1/chat/completions"
    MODEL = "qwen/qwen2.5-vl-7b"

    def generate(self, messages):
        payload = {
            "model": self.MODEL,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 1024,
        }

        response = requests.post(self.URL, json=payload)
        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]