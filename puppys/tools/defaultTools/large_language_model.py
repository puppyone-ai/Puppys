import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from puppys.env.func_env import FuncEnv
from puppys.llm.models import lite_llm_chat


def llm(
    prompt: str, 
    *, 
    model: str = "gpt-4o", 
    url: str = None, 
    temperature: float = 0.7, 
    max_tokens: int = 2048
) -> str:
    """
    Large_Language_Model, ChatGPT, GPT4 or GPT3.5,
    Good at summarizing, retrieving, finding information, generating text, and answer message based on a reference. etc.
    Bad for real-time information, webpage and generating image.

    For example:
    ## Summarizing the web based on the html
    prompt = f"What does this mean, summarize it into 100 words: {self.html}"
    result = llm(prompt=prompt)
    """

    model = model if model else os.environ.get("OPENAI_MODEL", "")

    url = url if url else os.getenv("OPENAI_BASE_URL", None)

    result = lite_llm_chat(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model=model,
        temperature=temperature,
        base_url=url,
        max_tokens=max_tokens
    )

    return result


if __name__ == "__main__":
    text = "How should I install the package of openAI"

    # Define the tool
    LLM = FuncEnv(
        value=llm, 
        name=llm.__name__, 
        description=llm.__doc__,
        free_params=["prompt"]
    )

    # Print the response from tool
    res = LLM(prompt=text)
    print(res)
