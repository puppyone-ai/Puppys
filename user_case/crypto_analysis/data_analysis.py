import os

# If you are a VS Code users:
import sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Change the API key to your own
# os.environ["OPENAI_API_KEY"] = ""

from puppys.pp.mei import Mei


def crypto_analysis_decisiontree(self):
    import pandas as pd

    btc_data = pd.read_csv("data/btc_data.csv")
    eth_data = pd.read_csv("data/eth_data.csv")

    self.do_check("Calculate the correlation function between BTC and ETH price, plot it, and send the result to me.", show_response= True)
    
    self.do_check("Calculate the one-sided Fourier transform and power spectral density (PSD) of BTC price and ETH prices, plot them in two subplots. Save the figure and send the result to me."
    , show_prompt=True, show_response= True)
    
    self.do_check("Plot the probability density distribution of BTC and ETH prices in two subplots. Save the figure and send the result to me", show_prompt=True, show_response= True)

data_analyzer = Mei(value=crypto_analysis_decisiontree)

data_analyzer.run()