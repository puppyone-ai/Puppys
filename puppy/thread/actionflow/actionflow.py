from puppy.environment.base import EnvBase
from puppy.thread.base import ThreadBase
from puppy.thread.actionflow.action import Action
from puppy.utils.parse import parse_code2list


# the intermediate env for governing the actionflow in the thread
class Actionflow(EnvBase):
    def __init__(self, thread_instance: ThreadBase = ThreadBase(), **kwargs):

        """
        {
            "EnvBase": {
                "name": "",
                "intro": "",
                "tag": "env",
                "__visibility": False
            }
        }
        """

        super().__init__(name="actionflow",
                         intro="an actionflow that governs all actionflow_list in the thread",
                         visible=False, **kwargs)

        self.__thread_instance = thread_instance

        self.pending_list = ActionflowList(name="pending_list", intro="a list of pending actions", visible=True)
        self.current_list = ActionflowList(name="current_list", intro="a list of current actions", visible=True)
        self.history_list = ActionflowList(name="history_list", intro="a list of history actions", visible=True)
        self.on_going = Action(name="on_going", intro="the action that is currently running", visible=True)

    @property
    def flow_dict(self):
        flow_dict = {}

        for key, value in self.detail.items():
            if isinstance(value, ActionflowList):
                flow_dict.update({key: value})

        return flow_dict

    # (decorator) Use to update the specific actionflow list
    def update(self, func) -> None:

        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        # retrieve the thread goal description from the docstring of func
        import inspect

        source_code = inspect.getsource(func)
        parsed_action = parse_code2list(source_code)
        func_name = func.__name__

        if func_name in self.flow_dict:
            if func_name == "pending_list":
                for action in parsed_action:
                    self.pending_list.append(action)

            elif func_name == "current_list":
                for action in parsed_action:
                    self.current_list.append(action)

            elif func_name == "history_list":
                for action in parsed_action:
                    self.history_list.append(action)
        else:
            raise KeyError(f"{func_name} not in actionflow flow list")

        return

    # get all actionflow cleared
    def clear_all(self) -> None:

        # clear all actionflow_list
        for flow in self.detail:
            if isinstance(flow, ActionflowList):
                flow.clear()

        # clear the on_going
        self.on_going = Action(name="on_going", intro="the action that is currently running", visible=True)

    # as a shortcut to print actionflow when running
    def show_status(self) -> None:
        print(f"\n\u2699 Actionflow ################################################################################")
        print("\nPending:")  # \U0001F51C
        print(self.pending_list.read)
        print("\nCurrent:")  # \U000025B6
        print(self.current_list.read)
        print("\nHistory:")  # \U0001F519
        print(self.history_list.read)

    def get_code(self, pending: bool = False, current: bool = False, history: bool = False) -> str:
        res = '''\n'''
        if pending:
            res += "\n".join(action.code for action in self.pending_list)
        if current:
            res += "\n".join(action.code for action in self.current_list)
        if history:
            res += "\n".join(action.code for action in self.history_list)

        return res if res else "No code found"

    # save the actionflow.history to a file
    def save_actionflow_history(self):
        # save the actionflow_history
        import os
        from datetime import datetime

        # get date and time
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d_%H-%M-%S")

        # create folder, if not exist
        folder_path = "user_case_history"
        os.makedirs(folder_path, exist_ok=True)

        # create a new file
        file_path = os.path.join(folder_path, f"user_case_history_{date_str}.txt")

        # Directly convert the Python object to a JSON string
        history = self.history_list.read

        # Write the JSON string to a file as agent log

        import json

        with open(file_path, "w") as file:

            try:
                json.dump(history, file, indent=4)

            except ValueError as e:
                print(e)


# the base class of actionflow
class ActionflowList(list, EnvBase):
    def __init__(self, iterable=None, *args, **kwargs):

        """
        {
            "EnvBase": {
                "name": "",
                "intro": "",
                "tag": "env",
                "__visibility": False
            }
        }
        """

        EnvBase.__init__(self, *args, **kwargs)

        if iterable:
            list.__init__(self, iterable)
        else:
            list.__init__(self, [])

        self.tag = "actionflow_list"

        self.visible = True

    # add an action to the end of the list
    def put_action(self, action: Action) -> None:
        return self.append(action)

    # pop an action from the start of list
    def pop_action(self) -> Action:
        return self.pop(0)

    @property
    def read(self) -> dict:
        return {action.name: action.expose for action in self}

    # (decorator) Use to update the specific actionflow list
    def update(self, func) -> None:

        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        #print("\n\U0001F525 Parsing the code-------------------------------------------------------------------------")

        import inspect

        source_code = inspect.getsource(func)
        parsed_action = parse_code2list(source_code)

        for action in parsed_action:
            self.append(action)

        return
