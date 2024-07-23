import os

# If you are a VS Code users:
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from puppys.pp.mei import Mei

# Change the API key to your own
# os.environ["OPENAI_API_KEY"] = ""

def hacker_news_decisiontree(self, url):

    self.do_check(f"go to the given {url}, save the page's HTML", show_response=True)

    self.do_check("show the top 10 news @llm, and send it to me", show_response=True)

    self.do_check("pick the news that related to Large Language Models, summarize all the news, and send it to me", show_response=True)


hacker_news = Mei(hacker_news_decisiontree)

# TODO test_run requires parameters
hacker_news.test_run(url="https://news.ycombinator.com/")

