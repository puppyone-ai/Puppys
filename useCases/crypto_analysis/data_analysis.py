from puppy.thread.main import Thread

Mei = Thread()

@Mei.actionflow.update
def pending_list():
    ## we have "data/btc_data.csv" and "data/btc_data.csv" in the directory of this file.
    # read the data from the csv files and put them into dataframes.
    Mei.do()

    ## explore the data, check the first 5 rows of the dataframes and print them @python, and send to me
    Mei.do()
    send_message_to_human(top_five_rows)

    ## set and import the plotly library
    import matplotlib.pylab as plt

    ## calculate the correlation function between BTC and ETH price.
    # plot the correlation, and save it to the working directory. 
    # don't show the plot in the python console.
    Mei.do()


Mei.run()
