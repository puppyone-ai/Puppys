from puppy.environment.func import FuncBase
from puppy.llm.openAI import open_ai_chat
import os


class GPT(FuncBase):

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
        self.func = self.gpt
        self.intro = """
        Large Language Models, use it when you want to generate text based on the input text by GPT3.5 or GPT4.
        
        For example:
        ## get how to install the package of openAI by GPT4
        prompt = f"How should I install the package of openAI, based on the document of its website HTML: {self.html}"
        result = gpt(prompt=prompt)
        """

    @staticmethod
    def gpt(prompt, model="gpt-3.5-turbo-0125", temperature=0.7, max_tokens=2048):

        result = open_ai_chat(prompt=[{"role": "user",
                                       "content": prompt}],
                              model=model,
                              temperature=temperature,
                              api_key=os.environ["OPENAI_API_KEY"],
                              max_tokens=max_tokens,
                              printing=True, stream=True)

        return result


if __name__ == "__main__":
    text = "how should I install the package of openAI"

    gpt = GPT()

    print(gpt.run(text))
