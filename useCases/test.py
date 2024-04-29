from puppy.thread.main import Thread
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


hacker_news = Thread()

@hacker_news.actionflow.update
def pending_list():

    ## anwer the question of "how does surface code work" @gpt and send the result to me
    hacker_news.do()

hacker_news.run()
