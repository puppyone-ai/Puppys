from serpapi import GoogleSearch


def SerpyGoogleSearch(test,location):
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


    import json

    ## get the 
    # Assuming 'data' is the JSON structure you provided
    # Replace 'your_json_string' with the actual JSON data
    organic_results = results["organic_results"]


    ## 
    if "answer_box" in results:
        answer_box=results["answer_box"]
    else:
        answer_box=[]

    if "organic_results" in results:
        organic_results = results["organic_results"]
    else:
        organic_results=[]
        
    final_answer=organic_results[:3]

    return final_answer,answer_box