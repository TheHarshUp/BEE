class Memory:
    def __init__(self):
        self.messages = []

    def add_user(self, message: str):
        self.messages.append({
            "role": "user",
            "content": message,
        })

    def add_assistant(self, message: str):
        self.messages.append({
            "role": "assistant",
            "content": message,
        })

    def add_tool_result(self, result: str):
        self.messages.append({
            "role": "user",
            "content": f"Tool result:\n{result}",
        })

    def get_messages(self):
        return self.messages