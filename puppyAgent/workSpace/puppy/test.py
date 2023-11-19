import re
import requests
import pandas as pd




from googleapiclient.discovery import build
import pprint

search_content = "1+1=?"

my_api_key = "AIzaSyAr6hD-hcBxHUd2HGco-av94QxMT516Bec"
my_cse_id = "c7f01980ba6754447"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

results = google_search(search_content, my_api_key, my_cse_id, num=10)
for result in results:
    pprint.pprint(result)


