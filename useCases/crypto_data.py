import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from puppy import Puppy


# change the API key to your own
os.environ["OPENAI_API_KEY"] = "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"


Mei = Puppy(name="CryptoAnalysist")

@Mei.mainthread
def actionflow_pending():

    ## today is 2024-Apr-12, please fetch YTD of BTC and ETH from Yahoo finance `yfinance` @python
    Mei.do()
    
    ## save the data to a csv file @python
    Mei.do()

    ## plot the price of BTC and ETH in the same graph @python
    Mei.do()

    ## calculate the correlation between BTC and ETH price and plot the function @python
    Mei.do()

Mei.run()

