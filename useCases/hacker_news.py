

# If you are a VS Code users:
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from puppy.thread.main import Thread
from puppy.thread.decisiontree.decisiontree import default_decisiontree
from puppy.thread.main import thread_run



# change the API key to your own
#os.environ["OPENAI_API_KEY"] = ""

hacker_news = Thread(decisiontree=default_decisiontree)

@hacker_news.actionflow.update
def pending_list():

    ## go to https://news.ycombinator.com/ show the HTML
    hacker_news.do()

    ## show the top 10 news @gpt, and send it to me
    hacker_news.do()

    ## pick the news that related to Large Language Models, summarize all the news, and print it
    hacker_news.do()

thread_run([hacker_news])
