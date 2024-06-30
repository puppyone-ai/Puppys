from puppy.pp.mei import Mei


def crypto_analysis_decisiontree(self):
    import pandas as pd
    btc_data = pd.read_csv('data/btc_data.csv')
    eth_data = pd.read_csv('data/eth_data.csv')

    return btc_data


data_analyzer = Mei(value=crypto_analysis_decisiontree)

data_analyzer.run()
