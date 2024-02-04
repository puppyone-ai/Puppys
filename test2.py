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

    ## 搜北京的天气
    XiaoMei.do()

    ## 十分钟之后把天气发给我
    XiaoMei.do()

XiaoMei.run()

