from puppy.thread.main import Thread
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


hacker_news = Thread()



@hacker_news.actionflow.pending_list.initialize
def pending():

    ## go to https://news.ycombinator.com/, save its HTML
    hacker_news.do()

    ## show the top 10 news and send message to the user GPT
    hacker_news.do()

    ## pick the news that related to Large Language Models, summerize all the news, and show it to me
    hacker_news.do()


hacker_news.run()