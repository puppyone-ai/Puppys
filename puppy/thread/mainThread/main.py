import inspect
import threading
from .actionflow import Actionflow
from .actions import Actions
from .actions_mllm import ActionsMLLM
#from ...publicFunc.default import ActionDefault
from .base import ThreadBase
from .Thread import MinimalThread


class MainThread(ThreadBase):
    def __init__(self, mllm: bool):

        super().__init__()

        if mllm:
            self.actions = ActionsMLLM(self)
        else:
            self.actions = Actions(thread_instance=self)
        
        # self.current_thread_name = "mainThread"
        # self.actionflow = Actionflow(self)

        self.child_threads = {}

        self.agent_var_func = {}

        self.agent_func = {}
        self.agent_var = {}

        self.environment = {"self": self}

        self.goal = ""

    # to get value from agentVar
    def __getattr__(self, attr):
        if attr in self.agent_var:
            return attr.value

        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")

    ## the templete of an func for agents
    class agent_func_template:
        def __init__(self, thread_instance, **kwargs):
            self.thread_instance = thread_instance
            self.name = "None"
            self.tag = "func"
            self.description = "nothing"
            self.example = """
            ## doing nothing
            pass
            """

        def __call__(self, **kwargs):
            self.run(**kwargs)

        def run(self, **kwargs):
            pass

    ## the templete of an func for agents
    class Agent_var_templete:
        def __init__(self, thread_instance, **kwargs):
            self.thread_instance = thread_instance
            self.name = "None"
            self.tag = "var"
            self.description = "nothing"
            self.value = None

    # TODO
    def add_new_func(self, func):
        pass

    # TODO
    def add_new_var(self, func):
        pass

    def new_agent_func(self, func):
        args = inspect.getfullargspec(func).args
        source_code=inspect.getsource(func)
        name=func.__name__

        newAgentFunc=self.agent_func_templateTemplete()


        print("name:")
        print(name)

        print("arg:")
        print(args)

        print("source_code:")
        print(source_code)

    def new_agent_var(self, func):
        args = inspect.getfullargspec(func).args
        source_code=inspect.getsource(func)
        name=func.__name__

        print("name:")
        print(name)

        print("arg:")
        print(args)

        print("source_code:")
        print(source_code)

    # to run the thread
    def mainthread_run(self):

        # start the code thread
        thread_code = threading.Thread(target=self.mainthread_decisiontree)
        thread_code.daemon = False
        thread_code.start()

        # end the code thread
        thread_code.join()

    # # for the wrapper of action
    # def mainthread(self, func):
    #     def wrapper(self, *args, **kwargs):
    #         # self.initialize()
    #         func(*args, **kwargs)
    #
    #     self.current_thread_name= "mainThread"
    #     source_code = inspect.getsource(func)
    #
    #     # if the function is action, initialize the actionFlow
    #     func_name=func.__name__
    #     if func_name == "actionflow_pending":
    #
    #         # get source code
    #         self.actionflow.initialize(source_code)
    #
    #         print("\U0001F3B2 Initialize Done")
    #         print("Initialized Function: "+func_name)
    #
    #
    #
    #     if func_name == "trigger":
    #         # TODO
    #         pass
    #
    #     # execute the function with wrapper
    #     return wrapper

    # TODO
    def construct(self, func):
        def wrapper(*args, **kwargs):

            func(*args, **kwargs)

        self.main_thread = MinimalThread()
        self.actionflow = self.main_thread.actionflow
        self.actions_current = self.actionflow.actions_current
        self.action_current = self.actionflow.action_current

        source_code = inspect.getsource(func)
        self.actionflow.load_actions(Actions(source_code=source_code).action_list)

        print("\U0001F3B2 Initialize Done")
        print("Initialized Function: " + func.__name__)

        return wrapper

    def exec_mode(self, code, mode="thread"):
        exec(code, self.environment)

    def save_actionflow_history(self):
        # save the actionflow_history
        import os
        from datetime import datetime
        import json

        # get date and time
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d_%H-%M-%S")

        # create folder, if not exist
        folder_path = "history"  # Corrected the folder name from 'histoty' to 'history'
        os.makedirs(folder_path, exist_ok=True)

        # create a new file
        file_path = os.path.join(folder_path, f"history_{date_str}.txt")

        # Directly convert the Python object to a JSON string
        pretty_json = json.dumps(self.actionflow.actionflow_history, indent=4)

        # Write the JSON string to a file
        with open(file_path, "w") as file:
            file.write(pretty_json)

    def mainthread_decisiontree(self):

        # import tools, for agents

        # loading actions
        from ...publicFunc.default import ActionDefault

        self.action_default = ActionDefault(code_thread_instance=self)
        self.send_message_to_human = self.action_default.send_message_to_human
        self.gpt = self.action_default.gpt
        self.mllm = self.action_default.mllm
        self.functions_description_and_example = self.action_default.get_info()

        # self.actionflow.actionflow_current_clear()

        #print(self.Vars)

        print("\U0001F4E5 Import Done")
        # start the action flow

        while self.actionflow.actionflow_current == [] and self.actionflow.actionflow_pending != []:

            print("\U0001F525 Action Start")

            # # STEP 1: load the action from actionFlowPending to actionFlowCurrent
            # self.actionflow.action_current_load()
            #
            # # STEP 2: delete the action from actionFlowPending
            # self.actionflow.actionflow_pending_remove_front()

            # STEP 1&2: load the action from actionFlowPending to actionFlowCurrent,
            # and delete the action from actionFlowPending

            self.actionflow.actionflow_current.append(self.actionflow.actionflow_pending.pop(0))

            print("\U0001F51C ActionFlowPending:")
            print(self.actionflow.actionflow_pending)
            print("\U000025B6 ActionFlowCurrentJSON:")
            print(self.actionflow.actionflow_current)
            print("\U0001F519 ActionFlowHistory:")
            print(self.actionflow.actionflow_history)

            while self.actionflow.actionflow_current:

                # STEP 3.1: check if the action is fixed, semi-fixed, or changeable

                self.actions_current = self.actionflow.actionflow_current[0]

                while self.actions_current:

                    action = self.actions_current.pop(0)

                    self.action_current = action

                    match action["status"]:
                        case "fixed":
                            pass

                        case "semi-fixed":
                            self.actions.do()

                        case "changeable":
                            pass
                
                    # STEP 3.2 load the action from actionCurrent to actionOnGoing
                    # if self.actionflow.actionflow_current:
                    #     self.actionflow.action_current_execute()
                    self.actionflow.action_on_going.put(action['comment+code'])

                    # STEP 3.3: load the action from actionOngoing and execute the code, and determine if the action is hidden
                    action_code = self.actionflow.action_on_going.get()

                    print("\n")
                    print("\U0001F697 Running Code ################################################################")
                    print(action_code)
                    print("################################################################################")

                    exec(action_code, self.environment)
                    self.actionflow.action_on_going.task_done()

                    # STEP 4: load the action from the actionFlowCurrent to the actionFlowHistory
                    # self.actionflow.actionflow_history_JSON += self.actionflow.actionflow_current_JSON[0]
                    # self.actionflow.actionflow_current_JSON.pop(0)

                    # self.actionflow.action_current_save()
                    self.actionflow.actionflow_history.append(action)

                # STEP 5: remove the action from the actionFlowCurrent
                # if self.actionflow.actionflow_current:
                #     self.actionflow.actionflow_current_remove_front()
                self.actionflow.actionflow_current.pop(0)

                # else:
                #     pass

            # else:
            #         pass

        print("Done")
        print(self.actionflow.actionflow_history)

        # save the actionflow_history to the folder of history

        #self.save_actionflow_history()


# class Puppy(MainThread):
#     def __init__(self, name="puppy"):
#
#         super().__init__()
#         self.puppy_name=name
#
#     def run(self):
#         self.mainthread_run()




