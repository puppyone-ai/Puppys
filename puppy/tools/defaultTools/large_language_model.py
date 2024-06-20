from litellm import completion
from puppy.decorator import new_func
from puppy.env.func_env import FuncEnv



def llm(prompt, *, model="gpt-3.5-turbo-0125", temperature=0.7, max_tokens=2048) -> str:

    """
    Large_Language_Model, ChatGPT, GPT4 or GPT3.5,
    Good at summarizing, retrieving, finding information, generating text, and answer message based on a reference. etc.
    Bad for real-time information, webpage and generating image.

    For example:
    ## summarizing the web based on the html
    prompt = f"What does this mean, summarize it into 100 words: {self.html}"
    result = llm(prompt=prompt)
    """

    result = completion(messages=[{"role": "user",
                                   "content": prompt}],
                        model=model,
                        temperature=temperature,
                        max_tokens=max_tokens)

    return result.choices[0].message.content


if __name__ == "__main__":
    text = "how should I install the package of openAI"

    LLM= FuncEnv(value=llm, name=llm.__name__, description=llm.__doc__,
                 free_params=["prompt"])

    res = LLM(prompt=text)
    print(res)
