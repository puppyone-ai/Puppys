from puppy.thread.main import Thread
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


hacker_news = Thread()

@hacker_news.actionflow.update
def pending_list():

    ##
    hacker_news.do()

    ## go to https://news.ycombinator.com/, save its HTML @python
    hacker_news.do()

    ## show the top 10 news @ChatLLM and send message to the user
    hacker_news.do()

    ## pick the news that related to Large Language Models, summerize all the news, and show it to me
    hacker_news.do()

    ## let me pick the news that related to Large Language Models, summerize all the news, and show it to me
    print("done")

hacker_news.run()