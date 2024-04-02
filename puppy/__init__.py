from .thread.mainThread.main import MainThread



class Puppy(MainThread):
    def __init__(self, name="", mllm=False):
        
        super().__init__(mllm=mllm)
        self.puppy_name = name

    def run(self):
        self.mainthread_run()



