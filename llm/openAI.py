from openai import OpenAI
from halo import Halo
import os




def OpenAIChat(prompt=[],
            temperature=0.1, max_token_num=4096, model_name="gpt-4-turbo-preview",
            ApiKey="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",
            emoji=False, num=1,
            printingMode=False, streamingMode=False
            ):

    os.environ["OPENAI_API_KEY"] = ApiKey

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ApiKey))

    if emoji == True:
        spinner = Halo(text='generating', spinner='moon')
        spinner.start()

    else:
        pass

    completion = client.chat.completions.create(
        model=model_name,
        messages=prompt,
        temperature=temperature,
        max_tokens=max_token_num,
        n=num,
        stream=streamingMode,
    )

    if emoji == True:
        spinner.stop()

    else:
        pass

    if printingMode == True:

        if streamingMode ==False:
            print(completion.choices[0].text)

        elif streamingMode==True:
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    print(chunk.choices[0].delta.content, end="")

    else:
        pass

    return completion.choices[0].text



response=OpenAIChat(prompt = [{"role": "user", "content": "Introduce yourself, with 100 words"}],
               printingMode= True, streamingMode=True)

print(response)
