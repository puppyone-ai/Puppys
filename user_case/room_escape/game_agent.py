from puppys.pp.main import Puppy
from puppys.env.func_env import FuncEnv
from game_tool import Tool
from puppys.tools.defaultTools import talk_with_human, llm
from puppys.pp.actions import do_check, check, do, rewrite


def create_game_tool():
    pass



class GameCreator(Puppy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = "GameCreator"
        self.description = "A puppys that could create tools for an room escape game."
        self.version = "0.0.1"

        # The first tool
        self.llm = FuncEnv(
            value=llm,
            name=llm.__name__,
            description=llm.__doc__
        )

        # The second tool
        self.talk_with_human = FuncEnv(
            value=talk_with_human,
            name=talk_with_human.__name__,
            description=talk_with_human.__doc__,
            fixed_params={"puppy": self}
        )

    def do_check(self, *args, **kwargs):
        """
        Do and Check the current action.
        """

        return do_check(self, *args, **kwargs)

    def check(self, *args, **kwargs):
        """
        Check the current action.
        """

        return check(self, *args, **kwargs)

    def do(self, *args, **kwargs):
        """
        Do the current action.
        """

        return do(self, *args, **kwargs)

    def rewrite(self, *args, **kwargs):
        """
        Rewrite the current action prompt.
        """

        return rewrite(self, *args, **kwargs)
