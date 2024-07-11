# If you are a VS Code users:
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os

from puppys.pp.mei import Mei

# change the API key to your own
# os.environ["OPENAI_API_KEY"] = ""

def hacker_news_decisiontree(self, url):
    def functioncode():
        for i in range(10):
            if url:
                print(url)
            elif i == 5:
                print(5)
            else:
                print("No URL")
    
    class abctest:
        def __init__(self):
            print("abc")
        def test(self):
            print("test")
    
    functioncode()
    abctest().test()
    a = """
    newline\n
    new\n
    line\n
    aaa\n\n
    """
    a_dict = {
        "a": "a", 
        "b": "b", 
        "c": "c"
    }

    self.do_check(f"go to the given {url}, save the page's HTML", show_response=True)
    if url:
        self.do_check("Show me the url link.", show_response=True)
    else:
        self.do_check("Ask human to provide the URL", show_response=True)
    # self.do_check("show the top 10 news @llm, and send it to me", show_response=True)

    # self.do_check("pick the news that related to Large Language Models, summarize all the news, and send it to me", show_response=True)


hacker_news = Mei(hacker_news_decisiontree)

hacker_news.run(url="https://news.ycombinator.com/")
