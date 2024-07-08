# If you are a VS Code users:
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from puppy.tools.search import search
from puppy.env.func_env import FuncEnv
from puppy.pp.mei import Mei


def decisiontree(self):
    self.abc = "abc"
    if self.abc:
        self.do_check("Get a list of 10 random characters from `abc`",show_prompt=True, show_response=True)
        self.do_check("Print out the list",show_prompt=True, show_response=True)
    self.do_check("Print out `Finish`",show_prompt=True, show_response=True)


search_bot = Mei(value=decisiontree)
search_bot.run()
