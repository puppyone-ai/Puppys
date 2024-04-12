import queue

from .base import ThreadBase
from .actionflow import DefaultActionflow, Actionflow
from .action import Action, parse_code2list
from puppy.publicFunc.default import FunctionsDefault
from puppy.thread.mainThread.do import check, reforge

import inspect
import threading


# TODO: Merge the essential elements between original MainThread and Thread
class Thread(ThreadBase):
    def __init__(self, **kwargs):

        super().__init__()

        # if 'puppy' in kwargs:
        #     self.puppy = kwargs['puppy']
        #     self.puppy_name = self.puppy.puppy_name
        # else:
        self.puppy_name = "Mei"  # the name is essential in the prompt

        #
        # if 'task' in kwargs:
        #     self.thread_name = kwargs['task']

        self.goal = ""
        self.exec_environment = {"self": self}

        # initialize the actionflow
        self._build_default_actionflow()

        # import default funcs into the thread
        self._import_default_funcs()

        print('initialized thread done')

    def _build_default_actionflow(self) -> None:

        self.actionflow_pending = Actionflow(iterable=[], thread_instance=self)
        self.actionflow_current = Actionflow(iterable=[], thread_instance=self)
        self.actionflow_history = Actionflow(iterable=[], thread_instance=self)
        self.action_on_going = queue.Queue()

    def _import_default_funcs(self) -> None:

        self.functions_description_and_example = FunctionsDefault(thread_instance=self).get_infos()

    def parse_and_load(self, func) -> callable:
        def wrapper(*args, **kwargs):

            func(*args, **kwargs)

        source_code = inspect.getsource(func)
        parsed_action = parse_code2list(source_code, thread_instance=self)

        for action in parsed_action:
            self.actionflow_pending.append(action)

        print("\U0001F3B2 Initialize Done")
        print("Initialized Function: " + func.__name__)

        return wrapper

    # TODO: re-organize the mainthread_decisiontree into thread and queue

    def default_decisiontree(self) -> None:

        # loading action

        print("\U0001F4E5 Import Done")
        # start the action flow

        while self.actionflow_pending:

            print("\U0001F525 Action Start")

            # STEP 1: take out the action from ActionFlowPending and put into ActionFlowCurrent

            action = self.actionflow_pending.pop_action()

            self.actionflow_current.put_action(action)

            print("\U0001F51C ActionFlowPending:")
            print(self.actionflow_pending)
            print("\U000025B6 ActionFlowCurrent:")
            print(self.actionflow_current)
            print("\U0001F519 ActionFlowHistory:")
            print(self.actionflow_history)

            # STEP 2:take out action from ActionFlowCurrent put into ActionOnGoing sequentially

            while self.actionflow_current:

                # STEP 2.1: load the action to action_on_going (for scalability in the future version)

                action = self.actionflow_current.pop_action()

                self.action_on_going.put(action)

                action = self.action_on_going.get()

                # STEP 3.1: check if the action is fixed, semi-fixed, or changeable
                if action["status"] == "fixed":
                    pass

                elif action["status"] == "semi-fixed":
                    self.do(action)

                # TODO: finish the changeable mode
                elif action["status"] == "changeable":
                    pass

                # STEP 4: load the action from the actionFlowCurrent to the actionFlowHistory
                self.actionflow_history.put_action(action)

        print("Done")
        print(self.actionflow_history)

        # TODO: save the actionflow_history to the folder of history

        # self.save_actionflow_history()

    def do(self, action) -> None:

        check(thread_instance=self, action=action, check_prompt=False)
        # n = 0

        if self.exec_environment["finishedOrNot"] == True:

            print("\n")
            print("\U0001F697 Running Code ################################################################")
            print(action["code"])
            print("################################################################################")

            exec(action["code"], self.exec_environment)

            action["status"] = "done"

            return

        else:
            # n += 1
            # print(f'reforging action:{action["name"]}, {n} times')
            reforge(thread_instance=self, action=action, plan_prompt=False)
            self.do(action)

    def run(self) -> None:
        # start the code thread
        thread_code = threading.Thread(target=self.default_decisiontree)
        thread_code.daemon = False
        thread_code.start()

        # end the code thread
        thread_code.join()

    # TODO: add wrapper to modify the property of the thread ,including create_function, add_vars
