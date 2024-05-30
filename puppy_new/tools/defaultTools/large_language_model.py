from puppy_new.environment.func import FuncBase
from litellm import completion


class LLM(FuncBase):

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

        self.name = "llm"
        self.func = self.lange_language_model
        self.intro = """
Large_Language_Model, ChatGPT, GPT4 or GPT3.5,
Good at summarizing, retrieving, finding information, generating text, and answer question based on a reference. etc.
Bad for real-time information, webpage and generating image.

For example:
## summarizing the web based on the html
prompt = f"What does this shows, summarize it into 100 words: {self.html}"
result = llm(prompt=prompt)
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

    chat = LLM()

    res = chat.run(text)

    print(res)
