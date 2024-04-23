from Puppys.puppy.publicFunc.default import Google_search_native


def google_search(search_content):
    """
    Serach Engine, use when you want to search something on google, return the title, link and snippet of the search result
    Example of use:
    search_content = "how should I intall the package of openAI"
    searchResults = self.GoogleSearchNative.run(search_content)
    """
    searcher = Google_search_native()
    results = searcher.search(search_content)
    result_simplified_list = []
    for result in results:
        result_simplified = {}
        result_simplified["title"] = result["title"]
        result_simplified["link"] = result["link"]
        result_simplified["snippet"] = result["snippet"]
        result_simplified_list.append(result_simplified)

    return result_simplified_list


def gpt():
    pass


def send_message_to_human():
    pass