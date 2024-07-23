from escape_tools import EscapeTool
from puppys.pp.main import Puppy
from puppys.env.func_env import FuncEnv
from user_case.room_escape.final.escape import escape


class Escaper(Puppy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = "Escaper"
        self.description = "A puppys that could play the game `room escape`."
        self.version = "0.0.1"

    def escape(self, *args, **kwargs):
        return escape(self, *args, **kwargs)


