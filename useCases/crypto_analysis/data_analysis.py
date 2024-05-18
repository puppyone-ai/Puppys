import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# change the API key to your own
#os.environ["OPENAI_API_KEY"] = ""


from puppy.thread.main import Thread

Mei = Thread()

@Mei.actionflow.update
def pending_list():
    ## we have "data/btc_data.csv" and "data/btc_data.csv" in a folder
    # read the data from the csv files and put them into dataframes.
    Mei.do()

    ## explore the data, check the first 5 rows of the dataframes and print them @python, and send to me
    Mei.do()
    send_message_to_human(top_five_rows)

    ## set and import the plotly library
    import matplotlib as plt

    ## calculate the correlation function between BTC and ETH price.
    # plot the correlation, and show it to me
    Mei.do()


Mei.run()
