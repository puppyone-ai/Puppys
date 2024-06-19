# If you are a VS Code users:
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# change the API key to your own
#os.environ["OPENAI_API_KEY"] = ""


from puppy.pp.main import Puppy
from puppy.tools.usable_tools import UsableTools
import pandas as pd

def crypto_analysis_decisiontree(self):

    self.btc_data = pd.read_csv('data/btc_data.csv')
    self.eth_data = pd.read_csv('data/eth_data.csv')

    self.do_check("show me the top 5 lines of the dataframes",show_response= True)

    print(self.btc_data.head)

    self.do_check("calculate the correlation function between BTC and ETH price(not only 5 lines, but all data), plot it, and send the result to me",show_response= True)

hacker_news = Puppy(decisiontree=crypto_analysis_decisiontree)

hacker_news.run()


