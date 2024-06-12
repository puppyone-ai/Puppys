from puppy.llm.openAI import open_ai_chat
import os

def Generate(context:list[str],query:str):
    prompt=[
        {
            "role":"system",
            "content":"""
            You are a helpful AI assistant answering the question based on the provided context.
            """
        },
        {
            "role":"user",
            "content":f"""
            context:{context}
            question:{query}
            """
        }
    ]

    final_answer = open_ai_chat(prompt=prompt,
                           model="gpt-4-turbo",
                           temperature=0.3,
                           api_key=os.environ["OPENAI_API_KEY"],
                           max_tokens=4096,
                           printing=True, stream=True)

    return final_answer