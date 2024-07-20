import os
from openai import OpenAI


# Using OpenAI API model
def open_ai_chat(
    prompt: list,
    temperature: float = 0.1, 
    max_tokens: int = 4096, 
    model: str = None,
    api_key: str = None,
    printing: bool = False, 
    stream: bool = True
) -> str:
    """
    Call the OpenAI API to get the Large Language Model's response.

    Args:
        prompt (str): The prompt to send to the LLM.
        temperature (float): The temperature of the LLM. The higher the temperature, the more random the output. The default is 0.1 for stable responses.
        max_tokens (int): The maximum number of tokens to generate. The default is 4096.
        model (str): The model to use for the LLM. Use the environment variable OPENAI_MODEL if not provided.
        api_key (str): The API key to use for the OpenAI API. Use the environment variable OPENAI_API_KEY if not provided.
        printing (bool): Whether to print the response. The default is False.
        stream (bool): Whether to stream the response. The default is True.

    Returns:
        str: The response from the LLM.
    """

    api_key = api_key if api_key else os.environ.get("OPENAI_API_KEY", api_key)
    client = OpenAI(api_key=api_key)

    model = model if model else os.environ.get("OPENAI_MODEL", model)

    completion = client.chat.completions.create(
        model=model,
        messages=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        n=1,
        stream=stream,
    )

    if printing:
        if not stream:
            print(completion.choices[0].message.content)
            print("\n")
            return completion.choices[0].message.content

        else:
            final_response = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="")
                    final_response += chunk.choices[0].delta.content

            print("\n")
            return final_response

    else:
        if not stream:
            return completion.choices[0].message.content

        else:
            final_response = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    final_response += chunk.choices[0].delta.content

            return final_response


if __name__ == "__main__":
    response = open_ai_chat(
        prompt=[{"role": "user", "content": "Introduce yourself, with 20 words"}],
        printing=False, 
        stream=True,
        api_key=os.environ["OPENAI_API_KEY"]
    )
