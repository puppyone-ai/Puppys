from puppy.environment.func import FuncBase
from puppy.llm.openAI import open_ai_chat
import os
from litellm import completion


class LangeLanguageModel(FuncBase):

    def __init__(self, *args, **kwargs):

        """
        {
            "FuncBase": {
                "name": "",
                "intro": "",
                "tag": "func",
                "__env_instance": None,
                "__func": None,
                "__visibility": True
            }
        }
        """

        super().__init__(*args, **kwargs)

        self.name = "gpt"
        self.func = self.lange_language_model
        self.intro = """
ChatGPT, GPT4 or GPT3.5,
ues it when summarizing text, HTML etc. Or generate text, answer question based on a reference. etc.

For example:
## summarizing the web based on the html
prompt = f"summarize this web based on the document of its website HTML: {self.html}"
result = gpt(prompt=prompt)
"""

    @staticmethod
    def lange_language_model(prompt, model="gpt-3.5-turbo-0125", temperature=0.7, max_tokens=2048):

        result = completion(messages=[{"role": "user",
                                       "content": prompt}],
                            model=model,
                            temperature=temperature,
                            max_tokens=max_tokens)

        return result.choices[0].message.content


if __name__ == "__main__":
    text = "how should I install the package of openAI"

    chat = LangeLanguageModel()

    res = chat.run(text)

    print(res)
