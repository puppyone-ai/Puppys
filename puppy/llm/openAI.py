from openai import OpenAI
from halo import Halo
import os

def OpenAIChat(prompt=[],
               temperature=0.1, max_tokens=4096, model="gpt-4-turbo-preview",
               api_key="",
               emoji=False, emojiText = "generating", spinner = "moon",
               printing=False, stream=False
               ):

    os.environ["OPENAI_API_KEY"] = api_key

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", api_key))

    if emoji == True:
        spinner = Halo(text=emojiText, spinner=spinner)
        spinner.start()

    else:
        pass

    completion = client.chat.completions.create(
        model=model,
        messages=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        n=1,
        stream=stream,
    )

    if emoji:
        spinner.stop()

    else:
        pass

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
                          api_key="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")

