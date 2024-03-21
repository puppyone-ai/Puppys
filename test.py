## TODO

"""
设置 thread 之间的 communication
"""

from puppy import Puppy


Xiao_Mei = Puppy(name="XiaoMei")


@Xiao_Mei.main_thread
def actionflow_pending():

    ## send me a message of hello, motherfucker after 10 seconds.
    Xiao_Mei.do()

    ## send the same message to me after 10 seconds
    Xiao_Mei.do()



Xiao_Mei.run()
