from zhipuai import ZhipuAI
import os

# using Zhipu API model
def ZhipuChat(prompt=[],
              temperature=0.1, max_tokens=4096, model="glm-4",
              api_key="",
              printing=False, stream=False
              ):

    os.environ["ZHIPU_API_KEY"] = api_key

    client = ZhipuAI(api_key=os.environ.get("ZHIPU_API_KEY", api_key))


    completion = client.chat.completions.create(
        model=model,
        messages=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
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
    response = ZhipuChat(prompt=[
                        {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的slogan"},
                        {"role": "assistant", "content": "当然，为了创作一个吸引人的slogan，请告诉我一些关于您产品的信息"},
                        {"role": "user", "content": "创造一个更精准、吸引人的slogan"}],
                        printing=True, stream=True, emoji=True,
                        api_key="938d656b9770894fd640a2ab9725bbaf.6zOTpj2EcoznRkzD")

    #print(response)

