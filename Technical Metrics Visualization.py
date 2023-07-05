#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: vishalramvelu

"""

import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import talib


start_date = '2022-01-01'
end_date = '2022-12-31'

ticker = 'bac'


data = yf.download(ticker, start=start_date, end=end_date)

# Calculate Bollinger Bands

period = 20  # Number of days for the moving average
std_dev = 2  # Number of standard deviations for the bands

# Calculate middle band (20-day simple moving average)
data['Middle Band'] = data['Close'].rolling(window=period).mean()

# Calculate standard deviation over the same period
data['Std Dev'] = data['Close'].rolling(window=period).std()

# Calculate upper and lower bands
data['Upper Band'] = data['Middle Band'] + std_dev * data['Std Dev']
data['Lower Band'] = data['Middle Band'] - std_dev * data['Std Dev']



# Generate trading signals based on price crossing the bands
data['Signal'] = 0  
data.loc[data['Close'] > data['Upper Band'], 'Signal'] = -1  # Sell signal
data.loc[data['Close'] < data['Lower Band'], 'Signal'] = 1  # Buy signal

# Plotting the Bollinger Bands and signals
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='Close')
plt.plot(data['Middle Band'], label='Middle Band')
plt.plot(data['Upper Band'], label='Upper Band')
plt.plot(data['Lower Band'], label='Lower Band')
plt.plot(data[data['Signal'] == 1]['Close'], 'g^', markersize=10, label='Buy Signal')
plt.plot(data[data['Signal'] == -1]['Close'], 'rv', markersize=10, label='Sell Signal')
plt.title('Bollinger Bands')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()


# calculate bollinger bands 

data['macd'], data['macd_signal'], _ = talib.MACD(data['Adj Close'])

# Plot MACD and signal line

plt.figure(figsize=(12, 6))
plt.plot(data.index, data['macd'], label='MACD')
plt.plot(data.index, data['macd_signal'], label='Signal Line')

# Add title and labels
plt.title('MACD and Signal Line')
plt.xlabel('Date')
plt.ylabel('MACD')

plt.legend()

plt.show()


