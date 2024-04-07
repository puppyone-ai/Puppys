from .base import ThreadBase
from .actionflow import Actionflow


class MinimalThread(ThreadBase):
    def __init__(self):

        super().__init__()
        self.actionflow = Actionflow(self)
        self.child_threads = {}
        self.fixed = False


    # def action(self):


