import os
from openai import OpenAI


class GPT():
    def __init__(self, thread_instance, question='', **kwargs):
        self.thread_instance = thread_instance
        self.action_name= "GPT"
        self.description = "Large Language Models, use it when you want to generate text based on the input text by GPT3.5 or GPT4"
        self.example = """
        ## get how to install the package of openAI by GPT4
        text = "how should I install the package of openAI"
        result=self.GPT.run(content=text)
        """
        
        self.apiKey = "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"
        self.model_name = "gpt-4-1106-preview"
        self.max_tokens = 4096
        self.temperature = 0.7

    def get_example(self):
        return self.example
    
    def get_description(self):
        return self.description

    def model_name(self, model_name):
        self.model_name = model_name

    def apiKey(self, api_key):
        self.apiKey = api_key

    def run(self, text=""):
        self.text=text
        chat_model = ChatOpenAI()
        result=chat_model.invoke(self.text)
        return result

"""
if __name__ == "__main__":
    text = "how should I intall the package of openAI"
    ApiKey="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"
    os.environ["OPENAI_API_KEY"]=ApiKey

    GPT=GPT(text)
    results = GPT.run()
    print(results)


"""