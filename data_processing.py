#from curses import window
from praw import reddit
#import config #KEYS
#import tweet_key as tk #Twitter KEYS
import praw
import time
import requests
#import datanews
import requests
import json
import datetime as dt
import tweepy
import textblob
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from bs4 import BeautifulSoup
from pytrends.request import TrendReq
#plt.style.use('fivethirtyeight')
#from datetime import date

import datetime
from datetime import date
import pandas_datareader as web

import san
import yfinance as yf

import investpy


def index_dataUS(index:str, from_date:str, to_date:str):
    df = investpy.indices.get_index_historical_data(index='S&P 500',
                                        country='United States',
                                        from_date=from_date,
                                        to_date=to_date)
    return df

def economic_calendar():
    news_df = investpy.news.economic_calendar(time_zone=None, 
                                        time_filter='time_only', 
                                        countries=['United States'], 
                                        importances=None, 
                                        categories=None, 
                                        from_date=None,#'01/04/2022', 
                                        to_date=None)
    return news_df

def crypto_data(crypto:str, from_date:str, to_date:str):
    ohlc_df = san.get(
    "ohlcv/"+crypto,
    from_date=from_date,#"2017-01-01",
    to_date=to_date,#"2022-02-19",
    interval="1w"
    )
    
    return ohlc_df

def crypto_growth(crypto:str, from_date:str, to_date:str):
    net_growth_df = san.get(
    "network_growth/"+crypto,
    from_date=from_date,
    to_date=to_date,
    interval="1d"
    )
    return net_growth_df

#TODO check why is it only working with ethereum

def crypto_social_presence(crypto:str, from_date:str, to_date:str):
    net_growth_df = san.get(
    "twitter_followers/"+crypto,
    from_date=from_date,
    to_date=to_date,
    interval="1d"
    )
    return net_growth_df

def crypto_positive_sentiment(crypto:str, from_date:str, to_date:str):
    net_growth_df = san.get(
    "sentiment_positive_total/"+crypto,
    from_date=from_date,
    to_date=to_date,
    interval="1d"
    )
    return net_growth_df

def crypto_negative_sentiment(crypto:str, from_date:str, to_date:str):
    net_growth_df = san.get(
    "sentiment_negative_total/"+crypto,
    from_date=from_date,
    to_date=to_date,
    interval="1d"
    )
    return net_growth_df

def market_cap(crypto:str, from_date:str, to_date:str):
    net_growth_df = san.get(
    "marketcap_usd/"+crypto,
    from_date=from_date,
    to_date=to_date,
    interval="1d"
    )
    return net_growth_df

def porcentage_data():
    today = date.today()
    today = today.strftime("%d/%m/%Y")

    df_data = index_dataUS('c', '01/01/1950', today)
    #print(df_data)

    data = []

    for count, data_prices  in enumerate(zip(df_data.Close, df_data.Open), 0):
        #print((data_prices[0])-(data_prices[1]))*100
        daily_porcentage = ((data_prices[0]-data_prices[1])*100)/data_prices[0]
        #print(daily_porcentage)
        data.append(daily_porcentage)
    
    return data

def do_percentage(amount, total):
    return (amount*100)/total

def get_porc(list_):
    positive = 0
    negative = 0
    look_out = False

    for count, porc in enumerate(list_):
        results = []
        if look_out == True:
            look_out = False

            if porc >= 0:
                positive += 1
            
            else:
                negative += 1
        
        if porc <= 3:
            look_out = True
        
        pos = do_percentage(positive, len(list_)-1)
        neg = do_percentage(negative, len(list_)-1)

    results.append(pos)
    results.append(neg)

    return results

#print(porcentage_data())
# df = pd.read_csv('data/BTC_historical_data_clean.csv')
# df = df.replace(',','', regex=True)
# df.Date = pd.to_datetime(df.Date)
# df = df.set_index('Date')
# #print(df)
# df.index = df.index.date
# print(df)



# def crypto_amount_in_top_holders(crypto:str, from_date:str, to_date:str):
#     net_growth_df = san.get(
#     "amount_in_top_holders/"+crypto,
#     from_date=from_date,
#     to_date=to_date,
#     interval="1d"
#     )
#     return net_growth_df

#################
#TESTING
################

# s_p500 = yf.Ticker("SPY")
# s_p500 = s_p500.history(period='max')
# s_p500 = s_p500.drop(['Open', 'High', 'Low', 
# 'Volume', 'Dividends', 'Stock Splits'], axis=1)
# #print(s_p500)
# s_p500.index = s_p500.index.date
# #df.index = df.index.date
# print(s_p500)

# s_p500 = pd.read_csv('data/sp500_daily-1950-to-2022.csv')
# #s_p500.index = s_p500.index.date
# s_p500.Date = pd.to_datetime(s_p500.Date)
# s_p500 = s_p500.set_index('Date')
# #print(df)
# s_p500.index = s_p500.index.date
# # print(s_p500)

# # df = pd.read_csv('data/USREC.csv')
# # print(df)

# df2 = pd.read_csv('data/USREC.csv')
# df2 = df2.rename(columns={'DATE':'Date'})
# df2.Date = pd.to_datetime(df2.Date)
# df2 = df2.set_index('Date')
# #print(df)
# df2.index = df2.index.date

# # #print(df2.index[0], type(df2.index[0]))

# # x_test = ["2015-02-01", "2015-02-02", "2015-02-03", "2015-02-04", "2015-02-05",
# #             "2015-02-06", "2015-02-07", "2015-02-08", "2015-02-09", "2015-02-10",
# #             "2015-02-11", "2015-02-12", "2015-02-13", "2015-02-14", "2015-02-15",
# #             "2015-02-16", "2015-02-17", "2015-02-18", "2015-02-19", "2015-02-20",
# #             "2015-02-21", "2015-02-22", "2015-02-23", "2015-02-24", "2015-02-25",
# #             "2015-02-26", "2015-02-27", "2015-02-28"]

# #print(x_test[0], type(x_test[0]))

# SP500_RES= s_p500.merge(df2, how='inner',
#                 right_index = True, left_index=True)

# recessions = []
# runner = []
# for i, data in enumerate(zip(SP500_RES.index, SP500_RES.USREC)):
#     #print(i, data[0], data[1])
#     #print(df2.index)
#     if data[1] == 1 and SP500_RES.USREC[i-1] == 0:
#         runner.append(data[0])
#     if data[1] == 0 and SP500_RES.USREC[i-1] == 1:
#         runner.append(data[0])
#         #print(runner)
#         recessions.append(runner)
#         runner = []

# #print(recessions)
# #print(SP500_RES)
# for i in range(len(recessions)):
#     print(recessions[i][0], recessions[i][1])
#print(df2)

# df = pd.read_csv('data/FEDFUNDS.csv')
# #df = df.rename(columns={'oldName1': 'newName1', 'oldName2': 'newName2'})
# df = df.rename(columns={'DATE':'Date'})
# df.Date = pd.to_datetime(df.Date)
# df = df.set_index('Date')
# #print(df)
# df.index = df.index.date
# #print(df)
# # 
#df = pd.read_csv('data/WALCL.csv')
#print(df)



# SP500= s_p500.merge(df, how='inner',
#         right_index = True, left_index=True)
# #SP500 = pd.concat([df, s_p500])
# #SP500.to_csv(r'test1-sp')
# #SP500 = SP500.dropna()
# print(SP500)

# print(dff)
#print(crypto_data('bitcoin', '2013-01-01', '2022-02-20'))

# df_btc = crypto_data('bitcoin', '2013-01-01', '2022-02-20')
# df_btc.index = df_btc.index.date
# df_btc = df_btc.drop(['openPriceUsd', 'highPriceUsd', 'lowPriceUsd', 'volume', 'marketcap'], axis=1)
# start = datetime.datetime(2013, 1, 1)
# end = datetime.datetime(2022, 2, 20)
# SP500 = web.DataReader(['sp500'], 'fred', start, end)
# #print(SP500)

# SP500BTC = df_btc.merge(SP500, how='inner',
# right_index = True, left_index=True)
# #print(df_btc)
# print(SP500BTC)

# correlation = SP500BTC.corr()
# print(correlation)

# df_btc['sma'] = df_btc.closePriceUsd.rolling(window=21).mean()
# df_btc['ema'] = df_btc.closePriceUsd.ewm(span=20,adjust=False).mean()

# print(df_btc.head(25))

#print(crypto_data('ethereum', '2017-01-01', '2022-02-10'))

#print(crypto_holders())

#print(np.shape(df_btc.closePriceUsd))

# dates = len(df_btc.closePriceUsd)
# days = np.linspace(1, len(df_btc), num=len(df_btc))
# # print(days)
# # print(len(days), dates)

# coef = np.polyfit(days, df_btc.closePriceUsd, 1)
# equ = np.poly1d(coef)

# print(equ)

# plt.plot(days, equ(df_btc.closePriceUsd), color='r')

# plt.show()



def fitter(x, p1, p2):
    return p1*np.log(x) + p2

def get_trending_topics():
    pytrend = TrendReq()
    
    #trendingtoday = pytrend.today_searches(geo='GLOBAl')
    keywords = pytrend.suggestions(keyword='Facebook')
    trendingtoday = pytrend.top_charts(2021, hl='en-US', tz=300, geo='GLOBAL')
    df_trends = pd.DataFrame(trendingtoday)
    df = pd.DataFrame(keywords)
    print(df.head(5))
    print(df_trends.head(20))

def collect_trend_score(keyword, scalar):
    pytrend = TrendReq() 
    pytrend.build_payload(kw_list=[keyword])
    df = pytrend.interest_over_time()
    df[keyword] = scalar*df[keyword]
    return df

def get_binance_bars(symbol, interval, startTime, endTime):
 
    url = "https://api.binance.com/api/v3/klines"
 
    startTime = str(int(startTime.timestamp() * 1000))
    endTime = str(int(endTime.timestamp() * 1000))
    limit = '1000'
 
    req_params = {"symbol" : symbol, 'interval' : interval, 'startTime' : startTime, 'endTime' : endTime, 'limit' : limit}
 
    df = pd.DataFrame(json.loads(requests.get(url, params = req_params).text))
 
    if (len(df.index) == 0):
        return None
     
    df = df.iloc[:, 0:6]
    df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
 
    df.open      = df.open.astype("float")
    df.high      = df.high.astype("float")
    df.low       = df.low.astype("float")
    df.close     = df.close.astype("float")
    df.volume    = df.volume.astype("float")
    
    df['adj_close'] = df['close']
     
    df.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in df.datetime]
 
    return df

#TESTING DFs

#dff = get_binance_bars('BTCUSDT', '1d', dt.datetime(2020, 1, 1), dt.datetime(2022, 2, 1))

#df = collect_trend_score('bitcoin', 1000)

# fig = go.Figure()
# df1 = collect_trend_score('crypto', 1000)
# columns = df1.columns
# df2 = get_binance_bars('BTCUSDT', '1d', dt.datetime(2020, 1, 1), dt.datetime(2022, 2, 1))

# fig.add_trace(go.Scatter(x=df1.indices, y=columns[0],
#                 mode='lines',
#                 name='lines'))

# fig.add_trace(go.Scatter(x=df2.indices, y=df2.close,
#                 mode='lines',
#                 name='lines'))
# fig.show()

# print(df)

# def plot_trendin_sentiment(df1, df2):

#     plt.title('Trending sentiment vs Ethereum price')
#     plt.xlabel('Date')
#     plt.ylabel('Values')

#     columns = df1.columns
#     print(columns)

#     plt.plot(df1.index, df1[columns[0]], color='darkslategray', linewidth=2)
#     plt.plot(df2.index, df2.close, color='orange', linewidth=2)

#     plt.legend(['Trending', 'ETH price'], loc='upper left')

#     plt.savefig('telegram_crypto_bot/test.png')
    #plt.show()

#print(collect_trend_score('cryptocurrency'))

#get_trending_topics()

#plot_trendin_sentiment(dff, df)

# def initialize_reddit():
#     reddit = praw.Reddit(client_id = config.client_id,
#     client_secret = config.client_secret, user_agent = config.user_agent)
#     return reddit

# def show_data(input_text, coin):

#     if input_text == 'get coin':
#         return get_data(coin)

# def get_data(coin):
#     try:
#         web_page = requests.get('https://www.coingecko.com/en/coins/'+coin)
#     except:
#         return 'error, couldnt find that coin'
#     web_page = web_page.content
#     soup = BeautifulSoup(web_page, 'html.parser')
#     for child in soup.body.children:
#         try:
#             for i in child.children:
#                 try:
#                     price = i.div.span.text
#                     if '$' in price:
#                         return price
#                 except:
#                     None
#         except:
#             None

def format_price(price):
    price = price.split('$')
    price = price[1].replace(',','')
    return price

# def get_crypto_comments(subreddit):
#     reddit = initialize_reddit()
#     hot_post = reddit.subreddit(subreddit).new(limit = 200)
#     titles = []
#     for post in hot_post:
#         if post.score >= 500:
#             #print('#-----------------------------------------#------------------------------------#')
#             title = post.title.lower()
#             titles.append(title)
#     return titles

# def initialize_twitter():
    
#     authenticator = tweepy.OAuthHandler(tk.API_KEY, tk.API_KEY_SECRET)
#     authenticator.set_access_token(tk.ACCESS_TOKEN, tk.ACCESSS_TOKEN_SECRET)

#     api = tweepy.API(authenticator, wait_on_rate_limit=True)
    
#     return api

# def search_sentiment(coin:str):

#     api = initialize_twitter()

#     search = f'#{coin} -filter:retweets'

#     tweet_cursor = tweepy.Cursor(api.search_tweets, q=search, lang='en', 
#     tweet_mode='extended').items(100)

#     tweets = [tweet.full_text for tweet in tweet_cursor]

#     tweets_df = pd.DataFrame(tweets, columns=['Tweets'])

#     for _, row in tweets_df.iterrows():
#         row['Tweets'] = re.sub('http\S+', '', row['Tweets'])
#         row['Tweets'] = re.sub('#\S+', '', row['Tweets'])
#         row['Tweets'] = re.sub('@\S+', '', row['Tweets'])
#         row['Tweets'] = re.sub('\\n', '', row['Tweets'])
    
#     tweets_df['Polarity'] = tweets_df['Tweets'].map(lambda tweet: textblob.TextBlob(tweet).sentiment.polarity)

#     tweets_df['Result'] = tweets_df['Polarity'].map(lambda pol: '+' if pol > 0 else '-')

#     positive = tweets_df[tweets_df.Result == '+'].count()['Tweets']

#     negative = tweets_df[tweets_df.Result == '-'].count()['Tweets']

#     return positive, negative
