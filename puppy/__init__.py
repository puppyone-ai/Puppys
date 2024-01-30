from .thread.codeThread.main import CodeThread
from .thread.goalThread.main import GoalThread


class Puppy(CodeThread):
    def __init__(self, name=""):
        
        super().__init__()
        self.puppyName=name

    def run(self):
        self.codeThreadRun()



