def decisiontree(self):
    import pandas as pd
    btc_data = pd.read_csv('data/btc_data.csv')
    eth_data = pd.read_csv('data/eth_data.csv')
    import matplotlib.pyplot as plt
    
    # Calculate the correlation between BTC and ETH prices
    correlation = btc_data['Adj Close'].corr(eth_data['Adj Close'])
    
    # Plot the correlation
    plt.figure(figsize=(10, 5))
    plt.plot(btc_data['Date'], btc_data['Adj Close'], label='BTC Price')
    plt.plot(eth_data['Date'], eth_data['Adj Close'], label='ETH Price')
    plt.title(f'Correlation between BTC and ETH Prices: {correlation:.2f}')
    plt.xlabel('Date')
    plt.ylabel('Adjusted Close Price')
    plt.legend()
    plt.grid(True)
    plt.savefig('correlation_plot.png')
    plt.show()
    
    # Send the result to the user
    talk_with_human(message="The correlation plot has been saved and displayed.")
    
    import numpy as np
    
    # Calculate the one-sided Fourier transform for BTC and ETH prices
    btc_fft = np.fft.rfft(btc_data['Adj Close'])
    eth_fft = np.fft.rfft(eth_data['Adj Close'])
    
    # Calculate the power spectral density (PSD) for BTC and ETH
    btc_psd = np.abs(btc_fft) ** 2
    eth_psd = np.abs(eth_fft) ** 2
    
    # Frequency axis for the plots
    btc_freq = np.fft.rfftfreq(len(btc_data['Adj Close']))
    eth_freq = np.fft.rfftfreq(len(eth_data['Adj Close']))
    
    # Plotting the Fourier transform and PSD in subplots
    plt.figure(figsize=(14, 10))
    
    # Subplot for BTC
    plt.subplot(2, 2, 1)
    plt.plot(btc_freq, np.abs(btc_fft), label='BTC Fourier Transform')
    plt.title('BTC Fourier Transform')
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.legend()
    
    plt.subplot(2, 2, 2)
    plt.plot(btc_freq, btc_psd, label='BTC Power Spectral Density')
    plt.title('BTC Power Spectral Density')
    plt.xlabel('Frequency')
    plt.ylabel('Power')
    plt.grid(True)
    plt.legend()
    
    # Subplot for ETH
    plt.subplot(2, 2, 3)
    plt.plot(eth_freq, np.abs(eth_fft), label='ETH Fourier Transform')
    plt.title('ETH Fourier Transform')
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.legend()
    
    plt.subplot(2, 2, 4)
    plt.plot(eth_freq, eth_psd, label='ETH Power Spectral Density')
    plt.title('ETH Power Spectral Density')
    plt.xlabel('Frequency')
    plt.ylabel('Power')
    plt.grid(True)
    plt.legend()
    
    # Save the figure
    plt.savefig('fft_psd_plot.png')
    plt.show()
    
    # Send the result to the user
    talk_with_human(message="The Fourier transform and power spectral density plots have been saved and displayed.")
    
    # Importing necessary libraries for plotting
    import matplotlib.pyplot as plt
    import pandas as pd
    
    # Loading the data
    btc_data = pd.read_csv('data/btc_data.csv')
    eth_data = pd.read_csv('data/eth_data.csv')
    
    # Plotting the probability density distribution of BTC and ETH prices in two subplots
    plt.figure(figsize=(14, 7))
    
    # Subplot for BTC
    plt.subplot(1, 2, 1)
    btc_data['Adj Close'].plot(kind='density', label='BTC Density')
    plt.title('Probability Density Distribution of BTC Prices')
    plt.xlabel('Price')
    plt.ylabel('Density')
    plt.legend()
    
    # Subplot for ETH
    plt.subplot(1, 2, 2)
    eth_data['Adj Close'].plot(kind='density', label='ETH Density')
    plt.title('Probability Density Distribution of ETH Prices')
    plt.xlabel('Price')
    plt.ylabel('Density')
    plt.legend()
    
    # Save the figure
    plt.savefig('density_plot.png')
    plt.show()
    
    # Sending the result to the user
    talk_with_human(message="The probability density distribution plots for BTC and ETH have been saved and displayed.")
    
    
