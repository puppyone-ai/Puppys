from puppy.llm import m_chat
from puppy.thread.mainThread.base import Thread


class MLLM:
    def __init__(self, thread_instance: Thread,
                 model: str = None,
                 # **kwargs
                 ) -> None:
        self.name = "mllm"
        self.thread_instance = thread_instance
        self.description = "Large Language Models, use it when you want to generate text based on the input text by large language models, you must add 'self.mllm' in this func."
        self.example = """
        ## get how to install the package of openAI by GPT4
        prompt = f"How should I install the package of openAI, based on the document of its website HTML: {self.html}"
        result = self.mllm.run(prompt=prompt) 
        
        ## query about some interesting question
        prompt = f"What is the fastest animal?"
        result = self.mllm.run(prompt=prompt) # you must add 'self.' in this func.
        """

        self.model = model

    def get_name(self) -> str:
        return self.name

    def get_example(self) -> str:
        return self.example

    def get_description(self) -> str:
        return self.description

    def run(self, prompt="") -> str:

        result = m_chat(prompt=self.thread_instance)

        return result


if __name__ == "__main__":
    text = "how should I install the package of openAI"
    results = MLLM(text).run()
    print(results)
