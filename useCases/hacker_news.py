import sys
import os
from puppy import Puppy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Use mllm to change mode, example: Mei = Puppy(name="Mei", mllm=True), @mllm rather @gpt

Mei = Puppy(name="Mei")


# change the API key to your own
os.environ["OPENAI_API_KEY"] = "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"


@Mei.mainthread
def actionflow_pending():

    ## go to this website: "https://https://news.ycombinator.com/news/" , save its HTML. @python
    Mei.do()
    print(HTML_text)

    ## save the top 10 news name and their urls based on the HTML @gpt, and send the result to me
    Mei.do()


Mei.run()
