import os
from puppy import Puppy


# change the API key to your own
os.environ["OPENAI_API_KEY"] = "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"


Xiao_Mei = Puppy(name="XiaoMei")

@Xiao_Mei.mainthread
def actionflow_pending():

    ## send me a message of hello, motherfucker after 10 seconds.
    Xiao_Mei.do()

    ## send the same message to me after 10 seconds
    Xiao_Mei.do()


Xiao_Mei.run()
