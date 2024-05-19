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
        self.on_going = None

    @property
    def flow_dict(self) -> dict:
        """
        This property is used to return the dict of all actionflow_list
        """
        flow_dict = {}

        for key, value in self.detail_dict.items():
            if isinstance(value, ActionflowList):
                flow_dict.update({key: value})

        return flow_dict

    def update(self, func) -> None:
        """
        This decorator is used to update the specific list under the actionflow
        """

        # retrieve the thread goal description from the docstring of func
        self.__thread_instance.goal = func.__doc__

        # compile the source code of func into actions
        import inspect
        source_code = inspect.getsource(func)
        parsed_action = parse_code2list(source_code)
        func_name = func.__name__

        # load the actions into the specific list
        if func_name in self.flow_dict:
            actionflow_list = getattr(self, func_name)
            for action in parsed_action:
                actionflow_list.put_action(action)

        # if the func_name is not in the actionflow, raise an error
        else:
            raise KeyError(f"{func_name} not in actionflow")

    def clear_all(self) -> None:
        """
        This method is used to clear all actionflow_list
        """

        for flow in self.flow_dict.values():
            flow.clear()

    def show_status(self) -> None:
        """
        This method is used to print the actionflow
        """

        print(f"\n\u2699 Actionflow ################################################################################")

        for flow in self.flow_dict.values():
            print(f'\n{flow.name}:')
            print(flow.action_list)

        print('\n')

    def get_code(self, *args) -> str:
        """
        This method is used to get the code of action within the specific actionflow_list
        """

        res = '''\n'''

        for flow in args:
            if type(flow) != str:
                raise TypeError("target flow name must be assigned as a string")

            if flow in self.flow_dict:
                res += "\n".join(action.code for action in self.flow_dict[flow])

            else:
                raise KeyError(f"{flow} not in actionflow")

        return res

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

        # Directly expose the history as a JSON string
        history = self.history_list.expose(as_json=True)

        # Write the JSON string to a file as agent log

        with open(file_path, "w") as file:

            file.write(history)


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

    @property
    def action_list(self) -> list:
        return [action.name for action in self]

    # add an action to the end of the list
    def put_action(self, action: Action) -> None:
        self.add_env(action)
        self.append(action)

    # pop an action from the start of list
    def pop_action(self) -> Action:
        self.delete_env(env_instance=self[0])
        return self.pop(0)

    # (Decorator) Use to update the specific list
    def update(self, func) -> None:
        # print("\n\U0001F525 Parsing the code-----------------------------------------------------------------------")

        import inspect

        source_code = inspect.getsource(func)
        parsed_action = parse_code2list(source_code)

        for action in parsed_action:
            self.append(action)
