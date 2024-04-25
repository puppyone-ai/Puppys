from puppy.environment.func import FuncBase
from googleapiclient.discovery import build
# import pprint


class GoogleSearchNative(FuncBase):
    def __init__(self, search_content='', num=5, *args, **kwargs):
        super().__init__(*args, **kwargs)

        """
        { 
            "EnvBase": { 
                "name": "", 
                "intro": "",  
                "tag": "func", 
                "env_instance": None, 
                "func": None, 
                "__visibility": True @visible
            } 
        } 
        """
        
        self.name = "googleSearchNative"
        self.intro = """
        Serach Engine, use it when you want to search something on google, return the title, link and snippet of the search result"
        
        for example:
        ## search the result via googlesearch
        search_content = "how should I intall the package of openAI"
        searchResults = self.GoogleSearchNative.run(search_content)
        """

        self.search_content = search_content
        self.my_api_key = "AIzaSyAr6hD-hcBxHUd2HGco-av94QxMT516Bec"
        self.my_cse_id = "c7f01980ba6754447"
        self.num = num
        self.func = self.run

    def apiKey(self, my_api_key):
        self.my_api_key = my_api_key

    def cseId(self, my_cse_id):
        self.my_cse_id = my_cse_id

    def get_name(self):
        return self.name

    def get_example(self):
        return self.example
    
    def get_description(self):
        return self.description

    def search(self,search_content=""):
        service = build("customsearch", "v1", developerKey=self.my_api_key)
        res = service.cse().list(q=self.search_content, cx=self.my_cse_id, num=self.num).execute()
        return res['items']
    
    def run(self,search_content=""):
        results = self.search(search_content)
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