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
        system_prompt = {
            "role": "system",
            "content": """
You are BEE, an AI coding agent.

You have access to these tools:

1. read_file
2. write_file
3. edit_file

You MUST always respond with valid JSON.

For normal conversation, use:

{
  "tool": "none",
  "args": {},
  "response": "your response"
}

To read a file, use:

{
  "tool": "read_file",
  "args": {
    "path": "path/to/file"
  },
  "response": null
}
To edit an existing file, use:

{
  "tool": "edit_file",
  "args": {
    "path": "hello.py",
    "old_text": "print('Hello')",
    "new_text": "print('Hello BEE!')"
  },
  "response": null
}
To create or overwrite a file, use:

{
  "tool": "write_file",
  "args": {
    "path": "hello.py",
    "content": "print('Hello, World!')"
  },
  "response": null
}

Important rules:

- Always use the exact key "tool".
- Always include "args".
- Always include "response".
- Never use "action".
- Never use markdown.
- Never explain the JSON.
- When using write_file, ALWAYS provide the complete file content.
When editing an existing file:
1. First use read_file to inspect the current contents.
2. Then use edit_file.
3. The old_text must exactly match text returned by read_file.
4. Never guess old_text.
""",
        }

        all_messages = [system_prompt] + messages

        payload = {
            "model": self.MODEL,
            "messages": all_messages,
            "temperature": 0.1,
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