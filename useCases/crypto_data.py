import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from puppy import Puppy


# change the API key to your own
os.environ["OPENAI_API_KEY"] = "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"


Mei = Puppy(name="HackerNews_reporter")

@Mei.mainthread
def actionflow_pending():

    ## go to this website: https://www.binance.com/en/landing/data,
    Mei.do()
    print(HTML_text)

    ## show the top 10 news and their urls based on the HTML @gpt, and send the message to the user
    Mei.do()
    print(news_and_urls)


Mei.run()

