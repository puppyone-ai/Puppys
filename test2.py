## TODO

"""
设置 thread 之间的 communication
"""

from puppy import Puppy


XiaoMei = Puppy(name="XiaoMei")


@XiaoMei.codeThread
def actionFlow():

    ## 帮我查一下北京的天气
    beijing_weather ="sunny"
    XiaoMei.do()

    ## 判断一下 hebei_weather是否是晴天
    XiaoMei.do()

    ## 10 秒钟之后告诉我北京的天气是啥
    XiaoMei.do()



XiaoMei.run()


