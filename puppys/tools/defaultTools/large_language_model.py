import os

from litellm import completion

from puppys.env.func_env import FuncEnv


def llm(prompt, *, model="gpt-4o", url=None, temperature=0.7, max_tokens=2048) -> str:
    """
    Large_Language_Model, ChatGPT, GPT4 or GPT3.5,
    Good at summarizing, retrieving, finding information, generating text, and answer message based on a reference. etc.
    Bad for real-time information, webpage and generating image.

    For example:
    ## summarizing the web based on the html
    prompt = f"What does this mean, summarize it into 100 words: {self.html}"
    result = llm(prompt=prompt)
    """

    if model is None:
        model = os.environ["OPENAI_MODEL"]
    else:
        pass

    if url == None:
        url = os.getenv("OPENAI_BASE_URL")
    else:
        pass

    result = completion(messages=[{"role": "user",
                                   "content": prompt}],
                        model=model,
                        temperature=temperature,
                        base_url=url,
                        max_tokens=max_tokens)

    return result.choices[0].message.content


if __name__ == "__main__":
    text = "how should I install the package of openAI"

    # define the tool
    LLM = FuncEnv(value=llm, name=llm.__name__, description=llm.__doc__,
                  free_params=["prompt"])

    #print the response from tool
    res = LLM(prompt=text)
    print(res)
