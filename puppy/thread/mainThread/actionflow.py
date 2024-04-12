import queue
from .base import ThreadBase
from .action import Action


class DefaultActionflow:
    def __init__(self, thread_instance: ThreadBase = None):
        pass
        # self.pending = Actionflow(iterable=[], thread_instance=thread_instance)
        # self.current = Actionflow(iterable=[], thread_instance=thread_instance)
        # self.history = Actionflow(iterable=[], thread_instance=thread_instance)
        # self.on_going = queue.Queue()


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
            code += action["code"] + "\n"

        return code

