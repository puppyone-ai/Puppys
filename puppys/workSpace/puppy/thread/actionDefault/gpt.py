import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain



class GPT():
    def __init__(self, codeThreadInstance, question='',**kwargs):
        self.codeThreadInstance = codeThreadInstance
        self.name="GPT"
        self.description = "Large Language Models, use it when you want to generate text based on the input text by GPT3.5 or GPT4"
        self.example = """
        ## get how to install the package of openAI by GPT4
        text = "how should I install the package of openAI"
        result=puppy.GPT.run(content=text)# where the puppy is name, change it with your name
        """
        
        self.apiKey = "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"
        self.model_name = "gpt-4-1106-preview"
        self.max_tokens = 10000
        self.temperature = 0.7

    def getExample(self):
        return self.example
    
    def getDescription(self):  
        return self.description

    def modelName(self, model_name):
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
