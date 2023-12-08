import re
import requests
import pandas as pd
from googleapiclient.discovery import build
import pprint


class GoogleSearchNative:
    def __init__(self, search_content='', num=5,**kwargs):
        self.description = "Google Serach, use when you want to search something on google, return the title, link and snippet of the search result"
        self.example = """
        ## search the result via googlesearch
        search_content = "how should I intall the package of openAI"
        GoogleSearch=GoogleSearchNative(search_content)
        searchResults = GoogleSearch.run()
        """

        self.search_content = search_content
        self.my_api_key = "AIzaSyAr6hD-hcBxHUd2HGco-av94QxMT516Bec"
        self.my_cse_id = "c7f01980ba6754447"
        self.num = num

    def apiKey(self, my_api_key):
        self.my_api_key = my_api_key

    def cseId(self, my_cse_id):
        self.my_cse_id = my_cse_id

    def getExample(self):
        return self.example
    
    def getDescription(self):  
        return self.description

    def search(self):
        service = build("customsearch", "v1", developerKey=self.my_api_key)
        res = service.cse().list(q=self.search_content, cx=self.my_cse_id, num=self.num).execute()
        return res['items']
    
    def run(self):
        results = self.search()
        result_simplified_list=[]
        for result in results:
            result_simplified={}
            result_simplified["title"]=result["title"]
            result_simplified["link"]=result["link"]
            result_simplified["snippet"]=result["snippet"]
            result_simplified_list.append(result_simplified)
            
        return result_simplified_list

"""
if __name__ == "__main__":

    search_content = "how should I intall the package of openAI"

    my_api_key = "AIzaSyAr6hD-hcBxHUd2HGco-av94QxMT516Bec"
    my_cse_id = "c7f01980ba6754447"

    GoogleSearch=GoogleSearchNative(search_content)
    GoogleSearch.apiKey(my_api_key)
    GoogleSearch.cseId(my_cse_id)
    results = GoogleSearch.run()
    for e in results:
        print(e)

"""



        