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

        # the first tool
        self.llm = FuncEnv(value=llm,
                           name=llm.__name__,
                           description=llm.__doc__,
                           free_params=["prompt"])

        # the second tool
        self.talk_with_human = FuncEnv(value=talk_with_human,
                                       name=talk_with_human.__name__,
                                       description=talk_with_human.__doc__,
                                       fixed_params={"puppy": self},
                                       free_params=["text"])

    def do_check(self, *args, **kwargs):
        return do_check(self, *args, **kwargs)

    def check(self, *args, **kwargs):
        return check(self, *args, **kwargs)

    def do(self, *args, **kwargs):
        return do(self, *args, **kwargs)
