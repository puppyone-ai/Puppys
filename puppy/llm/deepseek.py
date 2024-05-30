import os

from .openAI import open_ai_chat


def deepseek_chat(prompt, 
                 temperature=0.1, max_tokens=4096, model="deepseek-chat",
                 api_key=None,
                 printing=False, stream=True):
    
    if api_key is None:
        api_key = os.getenv("DEEPSEEK_API_KEY", None)
        if api_key is None:
            raise ValueError("API key not provided")
    
        
    return open_ai_chat(prompt,
                        temperature=temperature, max_tokens=max_tokens, model=model,
                        api_key=api_key, 
                        printing=printing, stream=stream,
                        base_url="https://api.deepseek.com")

if __name__ == "__main__":
    response = deepseek_chat(prompt=[{"role": "user", "content": "Introduce yourself, with 20 words"}],
                             printing=True, stream=True)