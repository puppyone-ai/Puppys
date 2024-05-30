from openai import OpenAI
import os


# using OpenAI API model
def open_ai_chat(prompt,
                 temperature=0.1, max_tokens=4096, model="gpt-4-turbo",
                 api_key=None,
                 printing=False, stream=True,
                 base_url=None,
                 ):

    if api_key == None:
        api_key = os.environ.get("OPENAI_API_KEY", None)
        if api_key is None:
            raise ValueError("API key not provided")

    client = OpenAI(api_key=api_key, base_url=base_url)

    completion = client.chat.completions.create(
        model=model,
        messages=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        n=1,
        stream=stream,
    )

    if printing is True:

        if stream is False:
            print(completion.choices[0].message.content)
            print("\n")
            return completion.choices[0].message.content

        elif stream is True:
            finalResponse=""
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    print(chunk.choices[0].delta.content, end="")
                    finalResponse += chunk.choices[0].delta.content

            print("\n")
            return finalResponse

    else:
        return completion.choices[0].message.content


if __name__ == "__main__":
    response = open_ai_chat(prompt=[{"role": "user", "content": "Introduce yourself, with 20 words"}],
                            printing=True, stream=True,
                            api_key=os.environ["OPENAI_API_KEY"])

