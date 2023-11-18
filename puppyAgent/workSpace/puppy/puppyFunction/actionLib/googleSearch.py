from serpapi import GoogleSearch
import json

## Search for the top results

class SerpyGoogleSearch():
    def __init__(self,test,location="China",pickingNum=3):
        self.discription="This is a google search function, it can search for information via GoogleSearch, it's aviliable anytime you search"
        self.test=test
        self.location=location
        self.pickingNum=pickingNum
        self.apiKey="72b0b910c9b0c16277b7295ff1e271b945610f0e4dcec66359d9a91b344a56e1"

    def setDiscription(self,discription):
        self.discription=discription

    def setAPIKey(self,apiKey):
        self.apiKey=apiKey

    def run(self):

        params = {
        "q": self.test,
        "location": self.location,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": self.apiKey,
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
                if element["position"]<=self.pickingNum:
                    organic_results_brief.append("title:"+element["title"])
                    organic_results_brief.append("snippet:"+element["snippet"])
                    organic_results_brief.append("link:"+element["link"])

        else:
            organic_results=[]


        final_answer=answer_box+organic_results_brief

        return final_answer

    ## Rethink about the result
    def DistillateResult(result,discription):
        pass
        

search=SerpyGoogleSearch("How to make a robot")
print(search.run())