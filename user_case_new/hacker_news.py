# If you are a VS Code users:
#import sys
#import os
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from puppy_new.pp.main import Puppy
from puppy_new.tools.usable_tools import UsableTools

# change the API key to your own
#os.environ["OPENAI_API_KEY"] = ""

def hacker_news_decisiontree(self):
    self.tool_box=UsableTools()

    self.do_check("go to https://news.ycombinator.com/ show the HTML", show_response = True)

    self.do_check("show the top 10 news, and send it to me")

    self.do_check("pick the news that related to Large Language Models, summarize all the news, and send it to me")


hacker_news = Puppy(decisiontree=hacker_news_decisiontree)

hacker_news.run()
