from puppy.pp.main import Puppy
from puppy.tools.defaultTools import talk_with_human, llm
from puppy.pp.actions import do_check, check, do
from puppy.environment.func_env import FuncEnv, new_func


class Mei(Puppy):

    name = "Mei"
    description = "A puppy that could help to intelligent your code"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.talk_with_human = FuncEnv(value=talk_with_human,
                                       pre_filled_parameter={"from_puppy": self})

        self.llm = FuncEnv(value=llm,
                           pre_filled_parameter={'model': "gpt-3.5-turbo-0125", 'temperature': 0.7, 'max_tokens': 2048})

        self.sub_env_add("talk_with_human", "llm")

    def do_check(self, *args, **kwargs):
        return do_check(self, *args, **kwargs)

    def check(self, *args, **kwargs):
        return check(self, *args, **kwargs)

    def do(self, *args, **kwargs):
        return do(self, *args, **kwargs)
