# If you are a VS Code users:
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import os
import requests
from puppys.decorator import new_func
from puppys.llm.models import lite_llm_chat


def perplexity_search(
    query: str
) -> str:
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
            "content": f"{query}",
        },
    ]

    response = lite_llm_chat(
        messages=messages,
        api_key=os.environ["PERPLEXITY_API_KEY"],
        base_url="https://api.perplexity.ai",
        model="mistral-7b-instruct",
        printing=True,
        stream=True,
        temperature=0.9
    )
    return response


def google_search(
    query: str
) -> dict:
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": os.environ["GCP_API_KEY"],
        "cx": os.environ["CSE_ID"],
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise ValueError(f"Failed to get the search result from google, status code: {response.status_code}")
    return response.json()


@new_func(free_params=["query"])
def search(
    query: str
) -> dict:
    """
    Search Engine, use it when the user request to find some real-time information online.
    For example, when user want to know the weather, asset price or economy indicators.

    For example:
    ## search the weather in Amsterdam
    query = "what is the weather today in Amsterdam?"
    searchResults = search(query)
    """

    try:
        return perplexity_search(query)
    except Exception:
        return google_search(query)


if __name__ == "__main__":
    query = "what is the weather today in Amsterdam?"
    response = search(query=query)
    print(response)
