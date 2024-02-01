from puppy import Puppy


XiaoMei = Puppy(name="XiaoMei")



@XiaoMei.codeThread
def actionFlow():

    ## 帮我找一个文件夹
    XiaoMei.do()

    ## 把你的 historical actionflow 存到文件夹下
    XiaoMei.do()

XiaoMei.run()




"""
解决 exec 的 var 在跨文件不共享的问题
"""


"""
设置 thread 之间的 communication
"""



"""
设置 action 的 visiable 和 invisible 的性质
"""



