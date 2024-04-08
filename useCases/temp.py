import sys
import os
from puppy import Puppy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Use mllm to change mode, example: Mei = Puppy(name="Mei", mllm=True), @mllm rather @gpt

Mei = Puppy(name="Mei")

@Mei.construct
def peep_hackernews():

    ## go to this website:https://news.ycombinator.com/ , save its HTML. @python
    Mei.do()
    print(HTML_text)

    ## show the top 10 news name and their urls based on the HTML @gpt, and send the message to the user
    Mei.do()
    print(news_and_urls)


Mei.run()

# peep_hackernews()


# TODO
# fixed the bug of saving actionflow_history
