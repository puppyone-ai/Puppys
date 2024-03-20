from .thread.mainThread.main import MainThread



class Puppy(MainThread):
    def __init__(self, name=""):
        
        super().__init__()
        self.puppy_name=name

    def run(self):
        self.main_thread_run()



