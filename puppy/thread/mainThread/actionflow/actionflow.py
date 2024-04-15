import queue
from puppy.thread.mainThread.base import ThreadBase
from puppy.thread.mainThread.actionflow.action import Action


# the main class of Actionflow
class Actionflow:
    def __init__(self, thread_instance: ThreadBase = None):
        self.pending_list = ActionflowList(iterable=[], thread_instance=thread_instance)
        self.current_list = ActionflowList(iterable=[], thread_instance=thread_instance)
        self.history_list = ActionflowList(iterable=[], thread_instance=thread_instance)
        self.on_going = queue.Queue()

    # get all actionflow cleared
    def clear_all(self):
        self.pending_list.clear()
        self.current_list.clear()
        self.history_list.clear()
        self.on_going = queue.Queue()

    # as a shortcut to print actionflow when running
    def view(self):
        print(f"\n\u2699 Actionflow ")
        print(f"################################################################################")
        print("\nPending:")  # \U0001F51C
        print(self.pending_list)
        print("\nCurrent:")  # \U000025B6
        print(self.current_list)
        print("\nHistory:")  # \U0001F519
        print(self.history_list)


# the base class of actionflow
class ActionflowList(list):
    def __init__(self, iterable, thread_instance: ThreadBase = None):

        transformed = [str(item) for item in iterable]
        super().__init__(transformed)

        if thread_instance:
            self.thread_instance = thread_instance

    # print the actionflow
    def __str__(self):
        newline = '\n'
        return f"{newline.join(str(action) for action in self)}"

    # get the actionflow itself
    def get(self):
        return self

    # get the action in a list, default setting: -1 is the latest
    def get_action(self, num=-1) -> Action:
        return self[num]

    # add an action to the end of the list
    def put_action(self, action: Action) -> None:
        return self.append(action)

    # get and remove the latest action
    def pop_action(self) -> Action:
        return self.pop(0)

    # get all action's code in the actionflow
    def get_code_all(self):
        return "".join(action.code + "\n" for action in self)
