from goalThread.goal import GoalThread
from code.code import CodeThread

class Puppy:
    def __init__(self):
        self.goalThread = GoalThread()
        self.codeThread = CodeThread()

    @property
    def goalThread(self):
        return self.goalThread.goalThread
    
    @goalThread.setter
    def goalThread(self, value):
        self.goalThread = value

    @property
    def codeThread(self):
        return self.codeThread.codeThread


if __name__ == '__main__':
    Yuning = Puppy()

    @Yuning.codeThread
    def action():

        ## Invite people
        Yuning.do()

    def trigger():
        pass
    
    @Yuning.goalThread
    def action():
        pass
    
    
    Yuning.run()


