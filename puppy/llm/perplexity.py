from openai import OpenAI

import os


def perplexity_search(query):

    """
    Search Engine, use it when you want to search something on google, return the title, link and snippet of the search result"

    for example:
    ## search the result via search engine
    query = "how should I install the package of openAI"
    searchResults = SearchNative(query)
    """

    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user."
            ),
        },
        {
            "role": "user",
            "content": (
                f"{query}"
            ),
        },
    ]

    client = OpenAI(api_key=os.environ['PERPLEXITY_API_KEY'], base_url="https://api.perplexity.ai")

    # chat completion without streaming
    response = client.chat.completions.create(
        model="mistral-7b-instruct",
        messages=messages,
    )
    return response.choices[0].message.content

# # chat completion with streaming
# response_stream = client.chat.completions.create(
#     model="mistral-7b-instruct",
#     messages=messages,
#     stream=True,
# )
# for response in response_stream:
#     print(response)


if __name__ == "__main__":
    import puppy

    search_content = "How many stars are in the universe?"

    results = perplexity_search(search_content)

    print(results)

