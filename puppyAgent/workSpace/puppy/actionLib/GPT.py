import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI


class GPT():
    def __init__(self, text):
        self.description = "GPT, use when you want to generate text based on the input text by GPT3.5 or GPT4"
        self.example = """
        # generate text based on the input text
        text = "how should I intall the package of openAI"
        GPT=GPT(text)
        results = GPT.run()
        """
        self.text = text
        self.model_name = "gpt-4-1106-preview"
        self.max_tokens = 100000
        self.temperature = 0.7

    def modelName(self, model_name):
        self.model_name = model_name

    def run(self):
        llm=ChatOpenAI(temperature=self.temperature,max_tokens=self.max_tokens,model_name=self.model_name)
        ChatGPT=LLMChain(llm=llm, prompt= "what's the name of the USA's president?")
        result=ChatGPT.predict()

        return result
    
if __name__ == "__main__":
    text = "how should I intall the package of openAI"
    ApiKey="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"
    os.environ["OPENAI_API_KEY"]=ApiKey

    GPT=GPT(text)
    results = GPT.run()
    print(results)
        


