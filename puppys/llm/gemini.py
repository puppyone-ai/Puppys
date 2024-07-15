import os
from models import ChatModel

class GeminiChat(ChatModel):
    def __init__(self, api_key_env="GEMINI_API_KEY", model_default='gemini/gemini-1.5-pro-latest', **kwargs):
        super().__init__(api_key_env, model_default, **kwargs)

    def chat(self, prompt):
        from litellm import completion
        response = completion(
            model=self.model,
            messages=prompt
        )
        return self.print_response(response)