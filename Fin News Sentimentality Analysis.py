#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: vishalramvelu

"""


import os
import pandas as pd
import matplotlib.pyplot as plt
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import nltk
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#web scrape all financial news article headlines and add to news tables

finwiz_url = 'https://finviz.com/quote.ashx?t='
news_tables = {}
companies = ['AMZN', 'GOOG', 'JPM', 'PFE', 'WMT','BAC']
for company in companies:
    url = finwiz_url + company
    req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'})
    response = urlopen(req)    
    html = BeautifulSoup(response)
    news_table = html.find(id='news-table')
    news_tables[company] = news_table
    
    
# Read last x headlines for given company 

amzn = news_tables['BAC']
amzn_tr = amzn.findAll('tr')
for i, table_row in enumerate(amzn_tr):
 a_text = table_row.a.text
 td_text = table_row.td.text
 print(a_text)
 print(td_text)
 # Exit after printing 5 rows of data
 if i == 5:
     break
 
 
#Parse data to create new df with article headline attatched to time, date, and company ticker

parsed_news = []
for file_name, news_table in news_tables.items():
    for x in news_table.findAll('tr'):
        text = x.a.get_text() 
        date_scrape = x.td.text.split()
        # if the length of date_scrape is 1, load'time is the only element (exceptions/errors)
        if len(date_scrape) == 1:
            time = date_scrape[0]
            
        # else load date as the 1st element and time as the second    
        else:
            date = date_scrape[0]
            time = date_scrape[1]
    
        ticker = file_name.split('_')[0]
        parsed_news.append([ticker, date, time, text])
    

        
print(parsed_news[:5]) 


#Start analyzing financial headlines using sentiment intensity analyzer

vish = SentimentIntensityAnalyzer()
columns = ['ticker','date','time','headline']

#convert the big parsed list to a data frame which is easily accessible 
fin_news = pd.DataFrame(parsed_news, columns = columns)
sentimental_ranking = fin_news['headline'].apply(vish.polarity_scores).tolist()
sentimental_ranking_df = pd.DataFrame(sentimental_ranking)
fin_news = fin_news.join(sentimental_ranking_df, rsuffix = '_right')
fin_news['date'] = pd.to_datetime(fin_news.date).dt.date


pd.set_option('max_colwidth', None) # show full width of showing cols
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to multiple lines

print(fin_news)

#plot distirbution of NLTK readings into histogram

plt.rcParams['figure.figsize'] = [15, 6]  

average_daily = fin_news.groupby(['ticker', 'date'])['compound'].mean().unstack(level=0)
average_daily.plot(kind='bar')

plt.grid()
plt.show()












