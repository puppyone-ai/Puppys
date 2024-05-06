import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from puppy.thread.main import Thread


# change the API key to your own
os.environ["OPENAI_API_KEY"] = "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"


Mei = Thread()

    ## today is 2024-Apr-12, please fetch YTD of BTC and ETH from Yahoo finance `yfinance` @python
    # use pip to install dependencies you need
    # Mei.do()

    ## create a new temperary folder named "crypto_analysis" and save the data to a csv file @python
    # Mei.do()

@Mei.actionflow.update
def pending_list():
    ## go to the folder named "crypto_analysis", which contains the "btc_data.csv" and "eth_data.csv" @python
    # read the data from the csv files and put them into dataframes.
    Mei.do()

    ## explore the data, check the first 5 rows of the dataframes @python
    Mei.do()

    ## send the data to the OpenAI API for preview @gpt 
    Mei.do()

    ## generate code to calculate the correlation function between BTC and ETH price. @python
    # plot the correlation, don't display the figure, save it to the folder "crypto_analysis"
    Mei.do()


Mei.run()

