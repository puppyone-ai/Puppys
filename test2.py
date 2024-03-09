## TODO

"""
设置 thread 之间的 communication
"""

from puppy import Puppy


XiaoMei = Puppy(name="XiaoMei")


@XiaoMei.mainThread
def actionFlowPending():

    ## send me a message of hello after 1 minute.
    XiaoMei.do()


XiaoMei.run()
