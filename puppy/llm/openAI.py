from openai import OpenAI
import os

# using OpenAI API model
def OpenAIChat(prompt=[],
               temperature=0.1, max_tokens=4096, model="gpt-4-turbo-preview",
               api_key="",
               printing=False, stream=False
               ):

    os.environ["OPENAI_API_KEY"] = api_key

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", api_key))



    completion = client.chat.completions.create(
        model=model,
        messages=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        n=1,
        stream=stream,
    )


    if printing == True:

        if stream == False:
            print(completion.choices[0].message.content)
            print("\n")
            return completion.choices[0].message.content

        elif stream == True:
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
    response = OpenAIChat(prompt=[{"role": "user", "content": "Introduce yourself, with 20 words"}],
                          printing=True, stream=True, emoji=True,
                          api_key=os.environ["OPENAI_API_KEY"])

