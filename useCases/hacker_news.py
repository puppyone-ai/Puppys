import os
from puppy import Puppy


# change the API key to your own
os.environ["OPENAI_API_KEY"] = "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"


Mei = Puppy(name="HackerNews_reporter")

@Mei.mainthread
def actionflow_pending():

    ## go to this website:https://news.ycombinator.com/ , save its HTML. @python
    Mei.do()
    print(HTML_text)

    ## show the top 10 news and their urls based on the HTML @gpt, and send the message to the user
    Mei.do()
    print(news_and_urls)


Mei.run()

