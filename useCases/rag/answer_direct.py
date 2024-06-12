from puppy.llm.openAI import open_ai_chat
import os
def answer_direct(query):
    prompt = [
                {
                    "role": "system",
                    "content": """
                    You are an intelligent assistant. You can answer a question provided by the user directly.
                    """
                },
                {
                    "role":"user",
                    "content":f"""
                    Question:{query}
                    """
                }
            ]
    answer = open_ai_chat(prompt=prompt,
                            model="gpt-4-turbo",
                            temperature=0.3,
                            api_key=os.environ["OPENAI_API_KEY"],
                            max_tokens=4096,
                            printing=True, stream=True)
    return answer