from openai import OpenAI
from halo import Halo
import os


def OpenAIChat(prompt=[],
               temperature=0.1, max_token_num=4096, model_name="gpt-4-turbo-preview",
               ApiKey="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",
               emoji=False, emojiText = "generating", spinner = "moon",
               printingMode=False, streamingMode=False
               ):

    os.environ["OPENAI_API_KEY"] = ApiKey

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ApiKey))

    if emoji == True:
        spinner = Halo(text=emojiText, spinner=spinner)
        spinner.start()

    else:
        pass

    completion = client.chat.completions.create(
        model=model_name,
        messages=prompt,
        temperature=temperature,
        max_tokens=max_token_num,
        n=1,
        stream=streamingMode,
    )

    if emoji:
        spinner.stop()

    else:
        pass

    if printingMode == True:

        if streamingMode == False:
            print(completion.choices[0].message.content)
            print("\n")
            return completion.choices[0].message.content

        elif streamingMode == True:
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
                      printingMode=True, streamingMode=True, emoji=True)

