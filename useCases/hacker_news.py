import sys
import os
from puppy.thread.main import Thread
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# change the API key to your own
#os.environ["OPENAI_API_KEY"] = ""

hacker_news = Thread()

@hacker_news.actionflow.update
def pending_list():

    ## go to https://news.ycombinator.com/ show me the HTML
    hacker_news.do()

    ## show the top 10 news @gpt, and send message to me
    hacker_news.do()

    ## pick the news that related to Large Language Models, summerize all the news, and show it to me
    hacker_news.do()

hacker_news.run()