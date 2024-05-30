# If you are a VS Code users:
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# change the API key to your own
#os.environ["OPENAI_API_KEY"] = ""


from puppy_new.pp.main import Puppy
from puppy_new.tools.usable_tools import UsableTools


def crypto_analysis_decisiontree(self):
    self.tool_box=UsableTools()

    import pandas as pd
    btc_data = pd.read_csv('data/btc_data.csv')
    eth_data = pd.read_csv('data/eth_data.csv')

    self.do_check("show me the top 5 lines of the dataframes",show_response= True)

    self.do_check("calculate the correlation function between BTC and ETH price based on the data, save it, and send the result to me",show_response= True)


hacker_news = Puppy(decisiontree=crypto_analysis_decisiontree)

hacker_news.run()
