from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import os


ApiKey="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"
os.environ["OPENAI_API_KEY"]=ApiKey

llm = OpenAI()
chat_model = ChatOpenAI()

from langchain.schema import HumanMessage

text = "What would be a good company name for a company that makes colorful socks?"
messages = [HumanMessage(content=text)]

result=llm.invoke(text)
print(result)
# >> Feetful of Fun

result=chat_model.invoke(messages)
print(result)