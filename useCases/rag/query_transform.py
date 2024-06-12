import os
from openai import OpenAI
from puppy.llm.openAI import open_ai_chat

def query_transformation(query:str,num_query:int):
    prompt=[
        {
            "role":"system",
            "content":f"""
            You are an AI language model assistant. Your task is to generate {num_query} 
different versions of the given user question to retrieve relevant documents from a vector 
database. By generating multiple perspectives on the user question, your goal is to help
the user overcome some of the limitations of the distance-based similarity search. You will
always output a python list composed of serval strings such as ["What do you want from me?","How are you?"]
            """
        },

        {
            "role":"system",
            "content":f"""
            You are provided an example as follows:
            <example>:
            User's input:
            "Who won a championship more recently, the Red Sox or the Patriots?"

            your output:
            [
            "When was the last time the Red Sox won a championship?",
            "When was the last time the Patriots won a championship?"
            ]
            </example>
            """
        },

        {
            "role":"user",
            "content":query
        }

    ]
    multi_q= open_ai_chat(prompt=prompt,
                          model="gpt-4-turbo",
                          temperature=0.3,
                          api_key=os.environ["OPENAI_API_KEY"],
                          max_tokens=4096,
                          printing=True, stream=True)

    multi_q=eval(multi_q)

    #print(type(multi_q))
    return multi_q

if __name__ == "__main__":
    query_transformation("which is the best university in the China?",5)

