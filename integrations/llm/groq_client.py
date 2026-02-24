import os
from groq import Groq

class GroqClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found.")
        self.client = Groq(api_key=self.api_key)

    def chat(self, messages, model="llama-3.3-70b-versatile", tools=None):
        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto" if tools else None
        )
