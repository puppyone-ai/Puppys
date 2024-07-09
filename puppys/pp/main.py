import threading

from .actions import explore
from puppys.env import Env
from puppys.pp.actions.load_env import load_env
from puppys.pp.default_env.actionflow.actionflow import Actionflow
from puppys.pp.default_env.puppy_vars import PuppyVars


class Puppy(Env):
    """
    The main class of a puppy
    An agent must call this class
    """

    def __init__(self, value=None, *args,  printing_mode='terminal',  **kwargs):

        super().__init__(*args, **kwargs)

        self.name = "default_puppy"

        self.actionflow = Actionflow(self, function=value, printing_mode=printing_mode)

        self.puppy_vars = PuppyVars(self, global_dict=globals())

        self.env_node = self

    def explore(self, *args, **kwargs):
        return explore(self, *args, **kwargs)

    def load_env(self, *args, **kwargs):
        return load_env(self, *args, **kwargs)

    def run(self, **kwargs) -> None:
        """
        run the agent
        """
        # run the actionflow
        return self.actionflow.run(**kwargs)



def puppy_run(puppy_list: list):
    """
    Run all the agents in the list at the same time
    """
    threads = []

    # create and start threads
    for puppy in puppy_list:
        thread = threading.Thread(target=puppy.run)
        thread.daemon = False
        threads.append(thread)
        thread.start()

    # wait for threads to finish
    for thread in threads:
        thread.join()

