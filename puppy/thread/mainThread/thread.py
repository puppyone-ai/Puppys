from .base import ThreadBase
from .actionflow import Actionflow


# TODO: Merge the essential elements between MainThread and MinimalThread
class MinimalThread(ThreadBase):
    def __init__(self):

        super().__init__()

        self.goal = ""
        self.actions = None
        self.actionflow = Actionflow(self)

        self.child_threads = {}

        self.exec_environment = {"self": self}

        self.fixed = False


    # def action(self):


