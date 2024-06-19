from puppy.pp.main import Puppy
from puppy.tools.defaultTools import talk_with_human, llm
from puppy.pp.actions import do_check, check, do
from puppy.env.func_env import FuncEnv
from functools import partial
from puppy.utils.custom_partial import custom_partial


class Mei(Puppy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = "Mei"
        self.description = "A puppy that could help to intelligent your code"
        self.version = "0.0.1"
        self.llm = llm  # wrapped in the /puppy/tools/defaultTools/llm.py
        self.talk_with_human = FuncEnv(value=custom_partial(talk_with_human, self))

    def do_check(self, *args, **kwargs):
        return do_check(self, *args, **kwargs)

    def check(self, *args, **kwargs):
        return check(self, *args, **kwargs)

    def do(self, *args, **kwargs):
        return do(self, *args, **kwargs)
