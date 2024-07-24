from litellm import completion
from typing import List, Optional, Union, Dict

# using OpenAI API model


def chat(
    model: Optional[str] = 'gpt-4-turbo',
    messages: List = [],
    temperature: Optional[float] = 0.1,
    top_p: Optional[float] = None,
    n: Optional[int] = 1,
    stream: Optional[bool] = True,
    printing: Optional[bool] = False,
    stop=None,
    max_tokens: Optional[int] = 4096,
    presence_penalty: Optional[float] = None,
    frequency_penalty: Optional[float] = None,
    **kwargs,
    ):

    """
    Wrapper function to interact with LiteLLM's completion API with optional parameters.

    Parameters:
    - model (str, optional, defaulted to gpt-4-turbo): ID of the model to use.
    - messages (list): List of messages comprising the conversation so far.
    - max_tokens (int, optional, defaulted to 4096): Maximum number of tokens to generate.
    - temperature (float, optional, defaulted to 0.1): Sampling temperature.
    - top_p (float, optional): Nucleus sampling probability.
    - n (int, optional, defaulted to 1): Number of chat completion choices to generate.
    - stream (bool, optional): Whether to stream responses.
    - printing (bool, optional): Whether to print responses.
    - stop (str or list, optional): Sequences where the API will stop generating further tokens.
    - presence_penalty (float, optional): Penalty for new tokens based on their presence.
    - frequency_penalty (float, optional): Penalty for new tokens based on their frequency.
    - kwargs (dict, optional): Additional parameters for any LLMs API require.

    Returns:
    - response: Response from the LiteLLM API.
    """

    response = completion(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        n=n,
        stream=stream,
        top_p=top_p,
        stop=stop,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
        **kwargs
        )

    if printing is True:

        if stream is False:
            print(response.choices[0].message.content)
            print("\n")
            return response.choices[0].message.content

        elif stream is True:
            finalResponse=""
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    print(chunk.choices[0].delta.content, end="")
                    finalResponse += chunk.choices[0].delta.content

            print("\n")
            return finalResponse

    else:
        if stream is False:
            return response.choices[0].message.content

        elif stream is True:
            finalResponse = ""
            for chunk in response:
                if chunk.choices[0].delta.content is not None:

                    finalResponse += chunk.choices[0].delta.content

            return finalResponse


# The following main function is simply for testing  
if __name__ == "__main__":
    import os

    ## set ENV variables
    os.environ["OPENAI_API_KEY"] = ""

    response = chat(
        model="gpt-4-turbo",
        messages=[{ "content": "Hello, how are you?", "role": "user"}],
    )
    
    print(response)