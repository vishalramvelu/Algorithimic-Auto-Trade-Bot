#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: vishalramvelu
"""

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import yfinance as yf

#base algo using just moving average and momentum trading

# Set the start and end date
start_date = '2023-01-20'
end_date = '2023-06-20'

# Set the ticker
ticker = 'bac'

# Get the data
data = yf.download(ticker, start_date, end_date)

df = data.copy()  # Make a copy of the DataFrame to avoid modifying the original

# Print 5 rows
print(df.tail())

# plot adjusted closing price, 30-day moving average of stock price and volume to see change

df['Price_Moving_Avg'] = df['Adj Close'].rolling(window=30).mean()
df['Vol_Moving_Avg'] = df['Volume'].rolling(window=30).mean()

df = df[df['Price_Moving_Avg'].notna()]
print(df)

close_price = df['Adj Close']
mavgplot = df['Price_Moving_Avg']
vmagplot = df['Vol_Moving_Avg']

mpl.rc('figure', figsize=(15, 10))

plt.style.use('ggplot')

close_price.plot(label=ticker, legend=True)
mavgplot.plot(label='mavg 30d', legend=True)
vmagplot.plot(secondary_y=True, label='Volume avg 30d', legend=True)

df.loc[:, 'Price lower than MAVG'] = df['Price_Moving_Avg'].gt(df['Adj Close'])
df.loc[:, 'Volume higher than MAVG'] = df['Vol_Moving_Avg'].gt(df['Volume'])

print(df)

# test returns using backtesting

z = 1 
PL = 0.00
Start_Price = (df['Adj Close'].head(1))
Start_Price = float(Start_Price)
print("Start Price: ",Start_Price)
End_Price = (df['Adj Close'].tail(1))
End_Price = float(End_Price)
print("End Price: ",End_Price)
Return = (PL/Start_Price)
Return_Per = "{:.2%}".format(Return)

for index, row in df.iterrows():
    if row['Volume higher than MAVG'] == 1:
        if row['Price lower than MAVG'] == 1:
            if z == 1:
                print(index,row['Adj Close'],'- Buy')
                close_adj = row['Adj Close']
                PL = PL - close_adj
                z = z - 1
                
    else: 
        if row['Volume higher than MAVG'] == 0:
            if row['Price lower than MAVG'] == 0:
                if z == 0: 
                    print(index,row['Adj Close'],'- Sell')
                    close_adj = row['Adj Close']
                    PL = PL + close_adj
                    Return = (PL/Start_Price)
                    Return_Per = "{:.2%}".format(Return)
                    print("Total Profit/Loss $",round(PL,2))
                    print("Total Return % ", Return_Per,"\n")
                    z = z + 1
                    
Hold_Return = (End_Price - Start_Price)
Hold_Return_Per = "{:.2%}".format((End_Price - Start_Price) / Start_Price)

print("The overall base return over this period was: ", Hold_Return, "Or in other words", Hold_Return_Per)



