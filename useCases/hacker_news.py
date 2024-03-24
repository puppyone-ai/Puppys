import os
from puppy import Puppy


# change the API key to your own
os.environ["OPENAI_API_KEY"] = "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"


HackerNews_reporter = Puppy(name="HackerNews_reporter")

@HackerNews_reporter.mainthread
def actionflow_pending():

    ## go to this website:https://news.ycombinator.com/ , save its HTML.
    HackerNews_reporter.do()
    print(HTML_text)

    ## tell me what's the top 10 news and their urls based on the HTML @gpt
    HackerNews_reporter.do()


HackerNews_reporter.run()

