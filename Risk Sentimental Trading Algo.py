#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: vishalramvelu
"""

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import yfinance as yf
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import nltk
import talib
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#Trading algo using Momentum Trading, Moving Average, Risk Management (Position Sizing), Bollinger Bands, 
#Moving Average Convergence-Divergence (MACD) and Sentimental Analysis

# Stock market analysis code

# Pick the start and end date
start_date = '2023-01-20'
end_date = '2023-06-20'

# Choose tickers needed
tickers = ['AMZN', 'GOOG', 'JPM', 'PFE', 'WMT','BAC']

for ticker in tickers:
    
    # Get the data
    data = yf.download(ticker, start_date, end_date)
    
    df = data.copy()  # Make a copy of the DataFrame to avoid modifying the original
    
    # Calculate RSI
    delta = df['Adj Close'].diff()
    gain = delta.mask(delta < 0, 0)
    loss = -delta.mask(delta > 0, 0)
    
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    df['RSI'] = rsi
    
    
    df['Price_Moving_Avg'] = df['Adj Close'].rolling(window=30).mean()
    df['Vol_Moving_Avg'] = df['Volume'].rolling(window=30).mean()
    
    df = df[df['Price_Moving_Avg'].notna()]
    
    
    # Calculate Bollinger Bands
    
    std_dev = 2  # Number of standard deviations for the bands
    
    # Calculate middle band (20-day simple moving average)
    df['Middle Band'] = df['Adj Close'].rolling(window=20).mean()
    
    # Calculate standard deviation over the same period
    df['Std Dev'] = df['Adj Close'].rolling(window=20).std()
    
    # Calculate upper and lower bands
    df['Upper Band'] = df['Middle Band'] + std_dev * df['Std Dev']
    df['Lower Band'] = df['Middle Band'] - std_dev * df['Std Dev']
    
    
    # Calculate MACD
    
    df['macd'], df['macd_signal'], _ = talib.MACD(df['Adj Close'])
    
    
    
    
    # Sentiment analysis code
    
    def integrate_sentiment_analysis(ticker):
        finwiz_url = 'https://finviz.com/quote.ashx?t='
        news_tables = {}
    
        url = finwiz_url + ticker
        req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'})
        response = urlopen(req)
        html = BeautifulSoup(response)
        news_table = html.find(id='news-table')
        news_tables[ticker] = news_table
    
        parsed_news = []
        for file_name, news_table in news_tables.items():
            for x in news_table.findAll('tr'):
                text = x.a.get_text()
                date_scrape = x.td.text.split()
                if len(date_scrape) == 1:
                    time = date_scrape[0]
                else:
                    date = date_scrape[0]
                    time = date_scrape[1]
                ticker = file_name.split('_')[0]
                parsed_news.append([ticker, date, time, text])
    
        vish = SentimentIntensityAnalyzer()
        columns = ['ticker', 'date', 'time', 'headline']
        financial_news = pd.DataFrame(parsed_news, columns=columns)
        sentimental_ranking = financial_news['headline'].apply(vish.polarity_scores).tolist()
        sentimental_ranking_df = pd.DataFrame(sentimental_ranking)
        financial_news = financial_news.join(sentimental_ranking_df, rsuffix='_right')
        financial_news['date'] = pd.to_datetime(financial_news.date).dt.date
    
        return financial_news
    
    financial_news = integrate_sentiment_analysis(ticker)
    
    # plot adjusted closing price, 30-day moving average of stock price and volume to see change
    
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
    
    
    # risk management strategy -> position sizing
    risk_percentage = 0.02
    capital = 10000
    profit = 0
    
    
    # Returns using backtesting
    z = 1
    PL = 0.00
    Start_Price = float(df['Adj Close'].head(1))
    End_Price = float(df['Adj Close'].tail(1))
    
    for index, row in df.iterrows():
        if (
            (row['Volume higher than MAVG'] == 1
            and row['Price lower than MAVG'] == 1)
            or (row['Adj Close'] < row['Lower Band'] and row['macd'] > row['macd_signal'])  # Condition for buying: price below lower band and bullish crossover in MACD
            or any(financial_news[(financial_news['ticker'] == ticker) & (financial_news['date'] == index.date())]['compound'] > 0.5)  # Check severity of sentiment analysis
        ):
            if z == 1:
                print(index, row['Adj Close'], '- Buy')
                close_adj = row['Adj Close']
                position_size = (capital * risk_percentage) / close_adj  # Calculate position size based on risk percentage
                PL = PL - (close_adj * position_size)  # Update PL calculation with position size
                z = z - 1
        else:
            if (
               (row['Volume higher than MAVG'] == 0 and row['Price lower than MAVG'] == 0) 
               or (row['Adj Close'] > row['Upper Band'] and row['macd'] < row['macd_signal']) # Condition for selling: price above upper band and bearish crossover in MACD
               or any(financial_news[(financial_news['ticker'] == ticker) & (financial_news['date'] == index.date())]['compound'] < -0.4) # Check severity of sentiment analysis
               
           ):
                if z == 0:
                    print(index, row['Adj Close'], '- Sell')
                    close_adj = row['Adj Close']
                    PL = PL + (close_adj * position_size)  # Update PL calculation with position size
                    profit += PL #add any change to overall profit (or loss)
                    Return = (PL / Start_Price)
                    Return_Per = "{:.2%}".format(Return)
                    print("Total Profit/Loss $", round(PL, 2))
                    print("Total Return % ", Return_Per, "\n")
                    z = z + 1
                  
                    
    # calculate overall returns 
    
    Hold_Return = End_Price - Start_Price
    Hold_Return_Per = "{:.2%}".format(Hold_Return / Start_Price)
    Total_Return_Per = "{:.2%}".format(profit / Start_Price)
    
    
    print("The stock trading algo return for", ticker, "is: ", profit , "In percentage: ", Total_Return_Per)
    print("The full base return over this period for", ticker,"was:", Hold_Return, "Or in other words", Hold_Return_Per)
