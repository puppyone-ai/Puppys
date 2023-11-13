from serpapi import GoogleSearch
import json


def SerpyGoogleSearch(test,location,pickingNum=3):
    discription="This is a google search function, it can search for information via GoogleSearch, it's aviliable anytime you search"

    params = {
    "q": test,
    "location": location,
    "hl": "en",
    "gl": "us",
    "google_domain": "google.com",
    "api_key": "72b0b910c9b0c16277b7295ff1e271b945610f0e4dcec66359d9a91b344a56e1"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    ## get the 
    # Assuming 'data' is the JSON structure you provided
    # Replace 'your_json_string' with the actual JSON data
    organic_results = results["organic_results"]


    ## pickup the answer box and the organic results
    if "answer_box" in results:
        answer_box=results["answer_box"]
    else:
        answer_box=[]

    if "organic_results" in results:
        organic_results=results["organic_results"]

        ## pick the top3 results for the organic results
        organic_results_brief=[]

        for element in organic_results:
            if element["position"]<=pickingNum:
                organic_results_brief.append("title:"+element["title"])
                organic_results_brief.append("snippet:"+element["snippet"])
                organic_results_brief.append("link:"+element["link"])

    else:
        organic_results=[]


    final_answer=answer_box+organic_results_brief

    return final_answer


print(SerpyGoogleSearch('how to make a cake','New York'))