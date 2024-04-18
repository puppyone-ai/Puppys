from puppy.thread.thread import Thread
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


hacker_news = Thread()

@hacker_news.parse_and_load
def pending():

    ## go to this website:https://news.ycombinator.com/ , save its HTML. @python
    hacker_news.do()
    print(HTML_text)

    ## show the top 10 news name and their urls based on the HTML @gpt, and send the message to the user
    hacker_news.do()
    print(news_and_urls)

hacker_news.run()