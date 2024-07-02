# If you are a VS Code users:
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from puppy.tools.defaultTools import search
from puppy.env.func_env import FuncEnv
from puppy.pp.mei import Mei

# change the API key to your own
# os.environ['PERPLEXITY_API_KEY'] = ""
# os.environ["OPENAI_API_KEY"] = ""


def decisiontree(self):

    self.do_check("Today is 2024-5-26, search internet to find the top 10 meme coins ranked by their real-time current market capitalization.",show_prompt=True, show_response=True)

    self.do_check("Search for the top 10 meme crypto coins, including its current, marketcap, and 24h trading volume.")

    self.do_check("Make a list using the information of the top 10 meme crypto coins, and show it to me. ")


search_bot = Mei(value=decisiontree)

search_bot.search = search

search_bot.run()
