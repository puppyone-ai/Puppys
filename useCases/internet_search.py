import os
import sys
# change the API key to your own
os.environ['PERPLEXITY_API_KEY'] = "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"

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from puppy.thread.main import Thread
Mei = Thread()

@Mei.actionflow.update
def pending_list():
    ## Go to https://www.coingecko.com/learn/meme-coins-good-bad-ugly and show the HTML
    Mei.do()   
    ## Then give me a brief about the article and show it to me @gpt
    Mei.do()
    ## Today is 2024-5-26, search internet to find the top 10 meme crypto coins ranked by their real-time current market capitalization.
    ## Search relevant information of the top 10 meme crypto coins, including its current, marketcap, and 24h trading volume. @search
    Mei.do()
    ## Make a list using the information of the top 10 meme crypto coins, and show it to me. @gpt
    Mei.do()

Mei.run()
