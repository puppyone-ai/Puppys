from .thread.mainThread.main import MainThread
from .thread.goalThread.main import GoalThread


class Puppy(MainThread):
    def __init__(self, name=""):
        
        super().__init__()
        self.puppyName=name

    def run(self):
        self.main_thread_run()



