from .base import ThreadBase
from .actionflow import Actionflow
from .actions import Actions
from puppy.publicFunc.default import ActionDefault

import inspect
import threading


# TODO: Merge the essential elements between original MainThread and Thread
class Thread(ThreadBase):
    def __init__(self, **kwargs):

        super().__init__()

        if 'puppy_name' in kwargs:
            self.puppy_name = kwargs['puppy_name']
        else:
            self.puppy_name = "Mei"

        self.goal = ""
        self.actionflow = Actionflow(self)

        self.current_actions = []
        self.current_action = {}

        # self.child_threads = {}

        self.exec_environment = {"self": self}

        # import default actions for the thread
        self._import_default_actions()

    def _import_default_actions(self):

        self.action_default = ActionDefault(code_thread_instance=self)
        self.send_message_to_human = self.action_default.send_message_to_human
        self.gpt = self.action_default.gpt
        self.mllm = self.action_default.mllm
        self.functions_description_and_example = self.action_default.get_info()

    def parse_and_load(self, func):
        def wrapper(*args, **kwargs):

            func(*args, **kwargs)

        source_code = inspect.getsource(func)
        parsed_actions = Actions(source_code=source_code,llm='gpt')
        self.actionflow.pending.append(parsed_actions)

        print("\U0001F3B2 Initialize Done")
        print("Initialized Function: " + func.__name__)

        return wrapper

    # TODO: re-organize the mainthread_decisiontree into thread and queue

    def mainthread_decisiontree(self):

        # loading actions

        print("\U0001F4E5 Import Done")
        # start the action flow

        while self.actionflow.pending:

            print("\U0001F525 Action Start")

            # STEP 1: pop the top action from ActionFlowPending to the end of ActionFlowCurrent

            self.actionflow.current.append(self.actionflow.pending.popleft())

            print("\U0001F51C ActionFlowPending:")
            print(self.actionflow.pending)
            print("\U000025B6 ActionFlowCurrent:")
            print(self.actionflow.current)
            print("\U0001F519 ActionFlowHistory:")
            print(self.actionflow.history)

            # STEP 2:take out actions for ActionFlowCurrent and pick out action sequentially

            while self.actionflow.current:

                # STEP 2.1: load the actions to action_on_going (for scalability in the future version)

                self.actionflow.action_on_going.put(self.actionflow.current.popleft())

                self.current_actions = self.actionflow.action_on_going.get()

                while self.current_actions:

                    self.current_action = self.current_actions.actions_list.popleft()

                    self._trigger()

                    print('triggered action:', self.current_action["name"])

                    # STEP 4: load the action from the actionFlowCurrent to the actionFlowHistory
                    self.actionflow.history.append(self.current_action)


        print("Done")
        print(self.actionflow.history)

    def _trigger(self):
        # STEP 3.1: check if the action is fixed, semi-fixed, or changeable

        match self.current_action["status"]:

            case "fixed":
                pass

            case "semi-fixed":

                match self.current_action["llm"]:

                    case "gpt":
                        from .do import RethinkWithGPT
                        self.action_do = RethinkWithGPT(self).do

                        self.action_do()

                    case "mllm":
                        pass

            # TODO: finish the changeable mode

            case "changeable":
                pass

        print("\n")
        print("\U0001F697 Running Code ################################################################")
        print(self.current_action["code"])
        print("################################################################################")

        exec(self.current_action["code"], self.exec_environment)

    def run(self):
        # start the code thread
        thread_code = threading.Thread(target=self.mainthread_decisiontree)
        thread_code.daemon = False
        thread_code.start()

        # end the code thread
        thread_code.join()

    # TODO: save the actionflow_history to the folder of history

    # self.save_actionflow_history()

    # TODO: add wrapper to modify the property of the thread ,including create_function, add_vars


