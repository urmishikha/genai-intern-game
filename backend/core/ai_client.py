import os
import openai
from typing import Optional
class AIClient:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def ask(self, prompt: str, model: str = "gpt-3.5-turbo") -> str:
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"AI Error: {e}")
            return "NO"  # Fail safe