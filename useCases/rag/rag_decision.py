import os
from openai import OpenAI
from puppy.llm.openAI import open_ai_chat

def rag_decision(query:str):

    #return "yes" or "no"

    prompt=[
        {
            "role":"system",
            "content":"""
            You are an intelligent assistant. Given the following query, determine if additional information retrieval is needed to provide a comprehensive answer.
            """
        },

        {
            "role":"user",
            "content":f"""
            Query:{query}
            Do you need to perform additional information retrieval to answer this query? Return a python string object such as 'yes' or 'no'.
            """
        }

    ]
    decision= open_ai_chat(prompt=prompt,
                          model="gpt-4-turbo",
                          temperature=0.3,
                          api_key=os.environ["OPENAI_API_KEY"],
                          max_tokens=4096,
                          printing=True, stream=True)

if __name__ == "__main__":
    rag_decision("which is the best university in the China?")

