import os
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from puppy.thread.main import Thread


# change the API key to your own
#os.environ["OPENAI_API_KEY"] = ""

# 显示当前工作目录
print("current folder:", os.getcwd())
print("content:", os.listdir('.'))


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
    import matplotlib
    matplotlib.use('Agg')  # Use the 'Agg' backend for non-GUI use


    ## calculate the correlation function between BTC and ETH price.
    # plot the correlation, and save the figure"
    Mei.do()


Mei.run()