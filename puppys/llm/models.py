from litellm import completion
from typing import List, Optional, Union, Dict

# using OpenAI API model


def chat(
    model: Optional[str] = 'gpt-4-turbo',
    messages: List = [],
    timeout: Optional[Union[float, int]] = None,
    temperature: Optional[float] = 0.1,
    top_p: Optional[float] = None,
    n: Optional[int] = 1,
    stream: Optional[bool] = True,
    printing: Optional[bool] = False,
    stream_options: Optional[Dict] = None,
    stop=None,
    max_tokens: Optional[int] = 4096,
    presence_penalty: Optional[float] = None,
    frequency_penalty: Optional[float] = None,
    logit_bias: Optional[Dict] = None,
    user: Optional[str] = None,
    response_format: Optional[Dict] = None,
    seed: Optional[int] = None,
    tools: Optional[List] = None,
    tool_choice: Optional[str] = None,
    parallel_tool_calls: Optional[bool] = None,
    logprobs: Optional[bool] = None,
    top_logprobs: Optional[int] = None,
    deployment_id=None,
    functions: Optional[List] = None,
    function_call: Optional[str] = None,
    base_url: Optional[str] = None,
    api_version: Optional[str] = None,
    api_key: Optional[str] = None,
    model_list: Optional[List] = None,
    **kwargs,
    ):

    response = completion(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        n=n,
        stream=stream,
        timeout=timeout,
        top_p=top_p,
        stream_options=stream_options,
        stop=stop,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
        logit_bias=logit_bias,
        user=user,
        response_format=response_format,
        seed=seed,
        tools=tools,
        tool_choice=tool_choice,
        parallel_tool_calls=parallel_tool_calls,
        logprobs=logprobs,
        top_logprobs=top_logprobs,
        deployment_id=deployment_id,
        functions=functions,
        function_call=function_call,
        base_url=base_url,
        api_version=api_version,
        api_key=api_key,
        model_list=model_list,
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