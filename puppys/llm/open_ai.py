import os
from models import ChatModel

class OpenAIChat(ChatModel):
    def __init__(self, api_key_env="OPENAI_API_KEY", model_default=None, **kwargs):
        super().__init__(api_key_env, model_default, **kwargs)

    def chat(self, prompt):
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        completion = client.chat.completions.create(
            model=self.model or os.getenv("OPENAI_MODEL"),
            messages=prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            n=1,
            stream=self.stream,
        )
        return self.print_response(completion)