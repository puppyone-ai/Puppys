## TODO

"""
设置 thread 之间的 communication
"""

from puppy import Puppy


XiaoMei = Puppy(name="XiaoMei")


@XiaoMei.codeThread
def actionFlow():

    ## 帮我查一下北京的天气
    XiaoMei.do()

    ## 10 秒钟之后告诉我北京的天气是啥
    XiaoMei.do()



XiaoMei.run()

