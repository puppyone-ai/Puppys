from .base import ThreadBase
from puppy.thread.mainThread.actionflow.actionflow import Actionflow
from puppy.thread.mainThread.actionflow.action import parse_code2list
from puppy.publicFunc.default import FunctionsDefault
from puppy.thread.mainThread.do import check, achieve

import inspect
import threading


# TODO: Merge the essential elements between original MainThread and Thread
class Thread(ThreadBase):
    def __init__(self, **kwargs):

        super().__init__()

        # naming the thread
        self._naming(**kwargs)

        # set the env of the thread
        self.goal = ""
        self.exec_environment = {"self": self}

        # install the actionflow
        self._build_default_actionflow()

        # import default funcs into the thread and get the description and example
        self._import_default_funcs_and_infos()

        print(f"{self.thread_name}: Initialize and Done \U0001F3B2")

    def _naming(self, **kwargs):
        # if 'puppy' in kwargs:
        #     self.puppy = kwargs['puppy']
        #     self.puppy_name = self.puppy.puppy_name
        # else:
        self.puppy_name = "Mei"  # the name is essential in the prompt

        #
        if 'name' in kwargs:
            self.thread_name = kwargs['name']
            print(f'Created a thread as {self.thread_name}! ')

        else:
            self.thread_name = "Ur Thread"
            print(f'Created a thread !')

    # build the actionflow
    def _build_default_actionflow(self) -> None:

        self.actionflow = Actionflow(thread_instance=self)

    def _import_default_funcs(self) -> None:

        self.functions_description_and_example = FunctionsDefault(thread_instance=self).get_infos()

    def parse_and_load(self, func) -> callable:

        def wrapper(*args, **kwargs):

            func(*args, **kwargs)

        print("\n\U0001F525 Parsing the code---------------------------------------------------------------------------------")

        source_code = inspect.getsource(func)
        parsed_action = parse_code2list(source_code, thread_instance=self)

        for action in parsed_action:
            self.actionflow.pending_list.append(action)

        return wrapper

    # set the default decision tree for run the actionflow
    def default_decisiontree(self) -> None:

        # start the actionflow

        while self.actionflow.pending_list:

            print("\n\U0001F525 Actionflow Run ---------------------------------------------------------------------------------")

            # STEP 1: take out the action from ActionFlowPending and put into ActionFlowCurrent

            action = self.actionflow.pending_list.pop_action()

            self.actionflow.current_list.put_action(action)

            # STEP 2:take out action from ActionFlowCurrent put into ActionOnGoing sequentially

            while self.actionflow.current_list:

                # STEP 2.1: load the action to ActionOnGoing (for scalability in the future version)

                # print the actionflow
                self.actionflow.view()

                action = self.actionflow.current_list.pop_action()

                self.actionflow.on_going.put(action)

                action = self.actionflow.on_going.get()

                print("\n\U0001F4A4 Action Code")
                print("################################################################################")
                print(action.code)
                # print("################################################################################")

                # STEP 3.1: check if the action is fixed, semi-fixed, or changeable
                if action.status == "fixed":
                    exec(action.code, self.exec_environment)
                    self.actionflow.history_list.put_action(action)

                elif action.status == "semi-fixed":
                    self.do(action)

                # TODO: finish the changeable mode
                elif action.status == "changeable":
                    pass

        print("Done")
        print(self.actionflow.history_list)

        # TODO: save the actionflow.history_list to the folder of history

        # self.save_actionflow_history()

    def do(self, action) -> None:

        self.exec_environment["finishedOrNot"] = False

        check(thread_instance=self, action=action, show_prompt=False)

        # try action till this action has been achieved
        while self.exec_environment["finishedOrNot"] is not True:

            # generate and write the code that can achieve the given action
            achieve(thread_instance=self, action=action, show_prompt=False)

            # execute the generated code
            exec(action.code, self.exec_environment)

            # save the ran code to the actionflow_history
            self.actionflow.history_list.put_action(action)

            # check the action, return 'finishOrNot= True / False'
            check(thread_instance=self, action=action, show_prompt=False)

    def run(self) -> None:
        # start the code thread
        thread_code = threading.Thread(target=self.default_decisiontree)
        thread_code.daemon = False
        thread_code.start()

        # end the code thread
        thread_code.join()

    # TODO: add wrapper to modify the property of the thread ,including create_function, add_vars
