import os
import requests

from puppy.environment.func import FuncBase
from puppy.llm.perplexity import perplexity_search


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

        self.func = perplexity_search

    @staticmethod
    def google_search(query):

        """
                Search Engine, use it when you want to search something on google, return the title, link and snippet of the search result"

                for example:
                ## search the result via googlesearch
                search_content = "how should I install the package of openAI"
                searchResults = self.GoogleSearchNative.run(search_content)
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
