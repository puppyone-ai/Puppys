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


# the base class of actionflow
class ActionflowList(list):
    def __init__(self, iterable, thread_instance: ThreadBase = None):

        transformed = [str(item) for item in iterable]
        super().__init__(transformed)

        if thread_instance:
            self.thread_instance = thread_instance

    # get the actionflow itself
    def get(self):
        return self

    # get the action in a list, default setting: -1 is the latest
    def get_action(self, num=-1) -> Action:
        return self[num]

    # TODO providing an index to put the action here
    # add an action to the end of the list
    def put_action(self, action: Action) -> None:
        return self.append(action)

    # get and remove the latest action
    def pop_action(self) -> Action:
        return self.pop(0)

    # get all action's code in the actionflow
    def get_code_all(self):

        code = ""
        for action in self:
            code += action.code + "\n"

        return code

    def __str__(self):
        return f"[{', '.join(str(action) for action in self)}]"
