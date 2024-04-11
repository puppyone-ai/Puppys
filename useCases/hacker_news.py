import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from puppy import Puppy
# Use mllm to change mode, example: Mei = Puppy(name="Mei", mllm=True), @mllm rather @gpt


Mei = Puppy(name="Mei")


# change the API key to your own
os.environ["OPENAI_API_KEY"] = "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"


@Mei.mainthread
def actionflow_pending():

    ## go to this website: "https://https://news.ycombinator.com/news/" , save its HTML. @python
    Mei.do()
    print(HTML_text)


    ## show the top 10 news name and their urls based on the HTML @mllm, and send the message to the user

    Mei.do()


Mei.run()


# TODO
# fixed the bug of saving actionflow_history

