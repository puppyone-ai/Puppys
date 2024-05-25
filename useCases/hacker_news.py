import os
from puppy.thread.main import Thread

# change the API key to your own
#os.environ["OPENAI_API_KEY"] = ""

hacker_news = Thread()

@hacker_news.actionflow.update
def pending_list():

    ## go to https://news.ycombinator.com/ show the HTML
    hacker_news.do()

    ## show the top 10 news @gpt, and send it to me
    hacker_news.do()

    ## pick the news that related to Large Language Models, summarize all the news, and show it to me
    hacker_news.do()

hacker_news.run()
