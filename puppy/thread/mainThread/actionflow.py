import queue
from .base import ThreadBase
from .action import Action


class DefaultActionflow:
    def __init__(self, thread_instance: ThreadBase = None):
        self.pending_list = Actionflow(iterable=[], thread_instance=thread_instance)
        self.current_list = Actionflow(iterable=[], thread_instance=thread_instance)
        self.history_list = Actionflow(iterable=[], thread_instance=thread_instance)
        self.on_going = queue.Queue()

    # def __getattribute__(self, item):


class Actionflow(list):
    def __init__(self, iterable, thread_instance: ThreadBase = None):

        transformed = [str(item) for item in iterable]
        super().__init__(transformed)

        if thread_instance:
            self.thread_instance = thread_instance

        """
        action: action
        actionflow: [A,A,A]
        on_going: (A)
        """

    def put_action(self, action: Action) -> None:
        return self.append(action)

    def pop_action(self) -> Action:
        return self.pop(0)

    def get_code(self):

        code = ""

        for action in self:
            code += action.code + "\n"

        return code

