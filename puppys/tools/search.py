from openai import OpenAI
import os
import requests
from puppys.decorator import new_func
from puppys.pp.main import Puppy
from puppys.env.func_env import FuncEnv
from puppys.pp.actions.explore import explore


def perplexity_search(query):

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


def google_search(query):

    url = "https://www.googleapis.com/customsearch/v1"
    params = {"q": query,
              "key": os.environ['GCP_API_KEY'],
              "cx": os.environ['CSE_ID'],
              }
    print(params)
    response = requests.get(url, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(f"Failed to get the search result from google, status code: {response.status_code}")
    return response.json()


@new_func(free_params=["query"])
def search(query):
    """
    Search Engine, use it when the user request to find some real-time information online.
    For example, when user want to know the weather, asset price or economy indicators.

    for example:
    ## search the weather in Amsterdam
    query = "what is the weather today in Amsterdam?"
    searchResults = search(query)"""

    return perplexity_search(query)



if __name__ == "__main__":

    # define an agent
    puppy=Puppy(name="Puppy")

    # define the tool in the agent
    puppy.tools_search = search
    # run the tool
    print(explore(puppy, target=FuncEnv))


