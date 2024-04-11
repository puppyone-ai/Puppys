import queue
from .base import ThreadBase
from .actions import Actions


class Actionflow(list):
    def __init__(self, iterable, thread_instance: ThreadBase = None):

        transformed = [str(item) for item in iterable]
        super().__init__(transformed)

        if thread_instance:
            self.thread_instance = thread_instance

        """
        action: Actions
        actionflow: [A,A,A]
        on_going: (A)
        """

    def put_actions(self, actions: Actions) -> None:
        return self.append(actions)

    def pop_actions(self) -> Actions:
        return self.pop(0)

    def get_code(self):

        code = ""

        for actions in self:
            code += actions["code"] + "\n"

        return code

