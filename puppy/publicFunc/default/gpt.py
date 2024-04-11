import os
from puppy.llm.openAI import OpenAIChat
from puppy.thread.mainThread.base import ThreadBase


class GPT:
    def __init__(self, thread_instance: ThreadBase = ThreadBase(),
                 # , question='', **kwargs
                 ):
        self.thread_instance = thread_instance
        self.name = "gpt"
        self.description = "Large Language Models, use it when you want to generate text based on the input text by GPT3.5 or GPT4"
        self.example = """
        ## get how to install the package of openAI by GPT4
        prompt = f"How should I install the package of openAI, based on the document of its website HTML: {self.html}"
        result=self.gpt.run(prompt=prompt)
        """

        # self.model_name = "gpt-3.5-turbo-0125"
        # self.max_tokens = 4096
        # self.temperature = 0.7

    # def get_name(self):
    #     return self.name
    #
    # def get_example(self):
    #     return self.example
    #
    # def get_description(self):
    #     return self.description

    # def model_name(self, model_name):
    #     self.model_name = model_name
    #
    # def apiKey(self, api_key):
    #     self.apiKey = api_key

    @staticmethod
    def run(prompt="", model="gpt-3.5-turbo-0125", temperature=0.7, max_tokens=2048,
            # **kwargs
            ):

        result = OpenAIChat(prompt=[{"role": "user",
                                     "content": prompt}],
                            model=model,
                            temperature=temperature,
                            api_key=os.environ["OPENAI_API_KEY"],
                            max_tokens=max_tokens,
                            printing=True, stream=True)

        return result


if __name__ == "__main__":
    text = "how should I install the package of openAI"

    # GPT = GPT()
    results = GPT().run(prompt=text)
    print(results)
