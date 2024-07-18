import threading
from puppys.env import Env
from puppys.pp.default_env.puppy_vars import PuppyVars
from puppys.pp.default_env.actionflow.actionflow import Actionflow
from .actions import explore
from puppys.pp.actions.load_env import load_env


class Puppy(Env):
    """
    The main class of a puppy.
    An agent must call this class.
    """

    def __init__(
        self,
        value: any = None,
        *args,
        printing_mode: str = "terminal",
        save_actionflow: bool = True,
        save_instance: bool = True,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.name = "default_puppy"

        self.actionflow = Actionflow(
            self,
            function=value,
            printing_mode=printing_mode,
            save_actionflow=save_actionflow,
            save_instance=save_instance,
        )

        self.puppy_vars = PuppyVars(self, global_dict=globals())

        self.env_node = self

    def explore(self, *args, **kwargs) -> None:
        return explore(self, *args, **kwargs)

    def load_env(self, *args, **kwargs) -> None:
        return load_env(self, *args, **kwargs)

    def test_run(self, **kwargs) -> None:
        """
        Debug the agent
        """

        # Run the actionflow in test mode
        return self.actionflow.test_run(**kwargs)

    def run(self, **kwargs) -> None:
        """
        Run the agent
        """

        # Run the actionflow
        return self.actionflow.run(**kwargs)


def puppy_run(
    puppy_list: list
) -> None:
    """
    Run all the agents in the list at the same time
    """
    threads = []

    # Create and start threads
    for puppy in puppy_list:
        thread = threading.Thread(target=puppy.run)
        thread.daemon = False
        threads.append(thread)
        thread.start()

    # Wait for threads to finish
    for thread in threads:
        thread.join()
