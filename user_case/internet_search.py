# If you are a VS Code users:
# import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from puppy.tools.defaultTools import search
from puppy.env.func_env import FuncEnv
from puppy.pp.mei import Mei

# change the API key to your own
os.environ['PERPLEXITY_API_KEY'] = "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"
# os.environ["OPENAI_API_KEY"] = ""


def decisiontree(self):
    # set available default toolbox for the agent, including two functioons, LLM() and TalkWithHuman()

    self.do_check("Today is 2024-5-26, search internet to find the top 10 meme coins ranked by their real-time current market capitalization.", show_prompt=True, show_response=True)

    self.do_check("Search for the top 10 meme crypto coins, including its current, marketcap, and 24h trading volume.")

    self.do_check("Make a list using the information of the top 10 meme crypto coins, and show it to me. ")


search_bot = Mei(decisiontree)

search_bot.add(search)

search_bot.run()
