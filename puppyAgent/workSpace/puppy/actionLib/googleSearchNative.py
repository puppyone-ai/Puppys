import re
import requests
import pandas as pd


from googleapiclient.discovery import build
import pprint

class GoogleSearchNative:
    def __init__(self, search_content, my_api_key, my_cse_id, num=5,**kwargs):
        self.search_content = search_content
        self.my_api_key = my_api_key
        self.my_cse_id = my_cse_id
        self.num = num

    def google_search(self):
        service = build("customsearch", "v1", developerKey=self.my_api_key)
        res = service.cse().list(q=self.search_content, cx=self.my_cse_id, num=self.num).execute()
        return res['items']


if __name__ == "__main__":
    search_content = "who is the president of the united states?"

    my_api_key = "AIzaSyAr6hD-hcBxHUd2HGco-av94QxMT516Bec"
    my_cse_id = "c7f01980ba6754447"

    GoogleSearch=GoogleSearchNative(search_content, my_api_key, my_cse_id)
    results = GoogleSearch.google_search()
    result_simplified_list=[]
    for result in results:
        result_simplified={}
        result_simplified["title"]=result["title"]
        result_simplified["link"]=result["link"]
        result_simplified["snippet"]=result["snippet"]
        result_simplified_list.append(result_simplified)
        print(result_simplified)

#    print(result_simplified_list)

#    pprint.pprint(result)