from puppy.llm.mllm_chat import m_chat


class Pipe:
    def __init__(self, thread_instance,
                 model: str = None,
                 # **kwargs
                 ) -> None:
        self.thread_instance = thread_instance
        self.description = "Large Language Models, use it when you want to generate text based on the input text by large language models"
        self.example = """
        ## get how to install the package of openAI by GPT4
        prompt = f"How should I install the package of openAI, based on the document of its website HTML: {self.html}"
        result = self.pipe.run(prompt=prompt)
        """

        self.model = model

    def get_name(self) -> str:
        return self.__class__.__name__

    def get_example(self) -> str:
        return self.example

    def get_description(self) -> str:
        return self.description

    def run(self) -> str:

        result = m_chat(prompt=self.thread_instance)

        return result


if __name__ == "__main__":
    text = "how should I install the package of openAI"
    results = Pipe(text).run()
    print(results)
