from zhipuai import ZhipuAI
from halo import Halo
import os

def ZhipuChat(prompt=[],
               temperature=0.1, max_token_num=4096, model_name="glm-4",
               ApiKey="938d656b9770894fd640a2ab9725bbaf.6zOTpj2EcoznRkzD",
               emoji=False, emojiText = "generating", spinner = "moon",
               printingMode=False, streamingMode=False
               ):

    os.environ["ZHIPU_API_KEY"] = ApiKey

    client = ZhipuAI(api_key=os.environ.get("ZHIPU_API_KEY", ApiKey))

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
    response = ZhipuChat(prompt=[
                        {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的slogan"},
                        {"role": "assistant", "content": "当然，为了创作一个吸引人的slogan，请告诉我一些关于您产品的信息"},
                        {"role": "user", "content": "智谱AI开放平台"},
                        {"role": "assistant", "content": "智启未来，谱绘无限一智谱AI，让创新触手可及!"},
                        {"role": "user", "content": "创造一个更精准、吸引人的slogan"}],
                          printingMode=True, streamingMode=True, emoji=True)

    #print(response)

