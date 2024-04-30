import os
import requests
from openai import OpenAI
from puppy.environment.func import FuncBase


class SearchNative(FuncBase):
    def __init__(self, *args, **kwargs):

        """
        {
            "FuncBase": {
                "name": "",
                "intro": "",
                "tag": "func",
                "__env_instance": None,
                "__func": None,
                "__visibility": True
            }
        }
        """

        super().__init__(*args, **kwargs)

        self.func = self.perplexity_search

    @staticmethod
    def perplexity_search(query):

        """
        Search Engine, use it when you want to search some actual information online"

        for example:
        ## search the result via search engine
        query = "how should I install the package of openAI"
        information = SearchNative(query)
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

    @staticmethod
    def google_search(query):

        """
        Search Engine, use it when you want to search something from perplexity online

        for example:
        ## search the query
        search_content = "how should I install the package of openAI"
        searchResults = google_search(search_content)
        """

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


if __name__ == "__main__":

    search_content = "how’s the weather today in New York?"

    search = SearchNative()
    results = search.run(search_content)

    print(results)
