import os
from puppy import Puppy


# change the API key to your own
os.environ["OPENAI_API_KEY"] = "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"


Xiao_Mei = Puppy(name="XiaoMei")

@Xiao_Mei.mainthread
def actionflow_pending():

    ## go to this website:https://news.ycombinator.com/ , save its HTML.
    Xiao_Mei.do()
    print(HTML_text)

    ## tell me what's the top 10 news and their urls based on the HTML of HackerNews @gpt
    Xiao_Mei.do()


Xiao_Mei.run()

