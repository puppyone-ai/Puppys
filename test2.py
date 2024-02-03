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

    ## 问用户关于厦门的天气
    XiaoMei.do()

    ## 把你的 historical actionflow 存到文件夹下
    XiaoMei.do()

XiaoMei.run()
