from puppy.environment.func import FuncBase
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
Good at summarizing, retrieving, finding information, generating text, and answer question based on a reference. etc.
You should not use this function to get real-time information from internet.

For example:
## summarizing the web based on the html
prompt = f"What does this shows: {self.html}"
result = gpt(prompt=prompt)
"""

    @staticmethod
    def lange_language_model(prompt, model="gpt-3.5-turbo-0125", temperature=0.7, max_tokens=2048):

        result = None

        cnt = 0

        while result is None and cnt < 3:

            try:
                cnt += 1

                result = completion(messages=[{"role": "user",
                                               "content": prompt}],
                                    model=model,
                                    temperature=temperature,
                                    max_tokens=max_tokens)

                import time
                time.sleep(1)

            finally:
                return result.choices[0].message.content


if __name__ == "__main__":
    text = "how should I install the package of openAI"

    chat = LangeLanguageModel()

    res = chat.run(text)

    print(res)
