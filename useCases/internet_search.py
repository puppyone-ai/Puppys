import os
import sys
# change the API key to your own
os.environ['PERPLEXITY_API_KEY'] = "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"

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from puppy.thread.main import Thread

Mei = Thread()

@Mei.actionflow.update
def pending_list():
    ## find me the current weather in Amsterdam and send the message to me
    Mei.do()   

    # print


Mei.run()
