from puppy.environment.func import FuncBase
from puppy.llm.openAI import open_ai_chat
import os
from litellm import completion


class ChatLLM(FuncBase):

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

        self.name = "chat_llm"
        self.func = self.chat_llm
        self.intro = """
        Large Language Models, use it when you want to generate text based on the input.
        
        For example:
        ## get how to install the package of openAI by GPT4
        prompt = f"How should I install the package of openAI, based on the document of its website HTML: {self.html}"
        result = chat_llm(prompt=prompt)
        """

    @staticmethod
    def chat_llm(prompt, model="gpt-3.5-turbo-0125", temperature=0.7, max_tokens=2048):

        result = completion(messages=[{"role": "user",
                                       "content": prompt}],
                            model=model,
                            temperature=temperature,
                            max_tokens=max_tokens)

        return result.choices[0].message.content


if __name__ == "__main__":
    text = "how should I install the package of openAI"

    chat = ChatLLM()

    res = chat.run(text)

    print(res)
