import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from puppy.thread.main import Thread
Mei = Thread()

@Mei.actionflow.update
def pending_list():

    ## today is 2024-05-10,search the top 10 news about Ukraine from internet. @SearchNative
    Mei.do()

    ## save these news to a markdown file named "ukraine_news.md" @python
    # the news should contains the title, the source, the date, and the first 100 words of the news
    Mei.do()

    ## give me a prediction about what will happen in Ukraine in the next 3 months. @GPT
    Mei.do()

Mei.run()