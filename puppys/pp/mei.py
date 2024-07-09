from puppys.pp.main import Puppy
from puppys.tools.defaultTools import talk_with_human, llm
from puppys.pp.actions import do_check, check, do
from puppys.env.func_env import FuncEnv


class Mei(Puppy):
    """
    A default puppy that contains llm and talk_with_human tools, and do, check, and do_check actions
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = "Mei"
        self.description = "A puppys that could help to intelligent your code"
        self.version = "0.0.1"

        # the first tool
        self.llm = FuncEnv(value=llm,
                           name=llm.__name__,
                           description=llm.__doc__)

        # the second tool
        self.talk_with_human = FuncEnv(value=talk_with_human,
                                       name=talk_with_human.__name__,
                                       description=talk_with_human.__doc__,
                                       fixed_params={"puppy": self})

    def do_check(self, *args, **kwargs):
        return do_check(self, *args, **kwargs)

    def check(self, *args, **kwargs):
        return check(self, *args, **kwargs)

    def do(self, *args, **kwargs):
        return do(self, *args, **kwargs)
