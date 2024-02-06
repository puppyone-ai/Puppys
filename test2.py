## TODO

"""
设置 thread 之间的 communication
"""

"""
设置 action 的 visiable 和 invisible 的性质
"""







from puppy import Puppy


XiaoMei = Puppy(name="XiaoMei")



@XiaoMei.codeThread
def actionFlow():

    ## 10 秒钟之后告诉我北京的天气是啥
    XiaoMei.do()


XiaoMei.run()

