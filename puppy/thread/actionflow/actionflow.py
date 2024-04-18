import queue
from puppy.thread.base import ThreadBase
from puppy.thread.actionflow.action import Action
from puppy.thread.actionflow.action import parse_code2list

# the intermediate env for governing the actionflow in the thread
class Actionflow:
    def __init__(self, thread_instance: ThreadBase = None):

        if thread_instance:
            self.thread_instance = thread_instance

        self.pending_list = ActionflowList(iterable=[], thread_instance=thread_instance)
        self.current_list = ActionflowList(iterable=[], thread_instance=thread_instance)
        self.history_list = ActionflowList(iterable=[], thread_instance=thread_instance)
        self.on_going = queue.Queue()

    # get all actionflow cleared
    def clear_all(self) -> None:
        self.pending_list.clear()
        self.current_list.clear()
        self.history_list.clear()
        self.on_going = queue.Queue()

    # as a shortcut to print actionflow when running
    def view(self) -> None:
        print(f"\n\u2699 Actionflow ################################################################################")
        print("\nPending:")  # \U0001F51C
        print(self.pending_list)
        print("\nCurrent:")  # \U000025B6
        print(self.current_list)
        print("\nHistory:")  # \U0001F519
        print(self.history_list)

    def get_code(self, pending: bool = False, current: bool = False, history: bool = False) -> str:
        res = ""
        if pending:
            res += "".join(action.code for action in self.pending_list)
        if current:
            res += "".join(action.code for action in self.current_list)
        if history:
            res += "".join(action.code for action in self.history_list)
        return res


# the base class of actionflow
class ActionflowList(list):
    def __init__(self, iterable, thread_instance: ThreadBase = None):

        transformed = [str(item) for item in iterable]
        super().__init__(transformed)

        if thread_instance:
            self.thread_instance = thread_instance

    # print the actionflow
    def __str__(self) -> str:
        newline = '\n'
        return f"{newline.join(str(action.read) for action in self)}"


    # add an action to the end of the list
    def put_action(self, action: Action) -> None:
        return self.append(action)


    # pop an action from the start of list
    def pop_action(self) -> Action:
        return self.pop(0)


    @property
    def read(self) -> list:
        return [action.read for action in self]



    def initialize(self, func) -> None:

        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        print("\n\U0001F525 Parsing the code-------------------------------------------------------------------------")

        import inspect

        source_code = inspect.getsource(func)
        parsed_action = parse_code2list(source_code)

        self.clear()

        for action in parsed_action:
            self.append(action)

        return