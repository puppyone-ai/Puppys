import os
from loguru import logger

class ChatModel:
    def __init__(self, api_key_env, model_default, temperature=0.1, max_tokens=4096, stream=True, printing=False):
        self.api_key = os.getenv(api_key_env)
        self.model = model_default
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.stream = stream
        self.printing = printing

    def chat(self, prompt):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def print_response(self, response):
        if self.stream:
            final_response = ""
            for chunk in response:
                if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
                    if self.printing:
                        logger.info(chunk.choices[0].delta.content, end="")
                        # print(chunk.choices[0].delta.content, end="")
                    final_response += chunk.choices[0].delta.content
            if self.printing:
                print("\n")
            return final_response
        else:
            if self.printing:
                logger.info(response.choices[0].message.content)
                # print(response.choices[0].message.content)
                print("\n")
            return response.choices[0].message.content