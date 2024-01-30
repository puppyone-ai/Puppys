from puppys.puppy.thread.codeThread.main import CodeThread
from puppys.puppy.thread.goalThread.main import GoalThread


class Puppy(CodeThread):
    def __init__(self, name=""):
        
        super().__init__()
        self.puppyName=name

    def run(self):
        self.codeThreadRun()




XiaoMei = Puppy(name="XiaoMei")



@XiaoMei.codeThread
def actionFlow():

    ## 帮我找一个文件夹
    XiaoMei.do()

    ## 把你的 historical actionflow 存到文件夹下
    XiaoMei.do()

XiaoMei.run()