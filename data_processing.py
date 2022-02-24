from praw import reddit
#import config #KEYS
import tweet_key as tk #Twitter KEYS
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
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
#plt.style.use('fivethirtyeight')
from datetime import date

import san

def crypto_data(crypto:str, from_date:str, to_date:str):
    ohlc_df = san.get(
    "ohlc/"+crypto,
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

def crypto_holders(crypto:str, from_date:str, to_date:str):
    net_growth_df = san.get(
    "twitter_followers/"+crypto,
    from_date=from_date,
    to_date=to_date,
    interval="1d"
    )
    return net_growth_df

# print(crypto_data('ethereum', '2017-01-01', '2020-02-20'))
# print(crypto_growth('ethereum', '2017-01-01', '2022-02-10'))

#print(crypto_holders())

#print(ohlc_df.tail())

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

def plot_trendin_sentiment(df1, df2):

    plt.title('Trending sentiment vs Ethereum price')
    plt.xlabel('Date')
    plt.ylabel('Values')

    columns = df1.columns
    print(columns)

    plt.plot(df1.index, df1[columns[0]], color='darkslategray', linewidth=2)
    plt.plot(df2.index, df2.close, color='orange', linewidth=2)

    plt.legend(['Trending', 'ETH price'], loc='upper left')

    plt.savefig('telegram_crypto_bot/test.png')
    #plt.show()

#print(collect_trend_score('cryptocurrency'))

#get_trending_topics()

#plot_trendin_sentiment(dff, df)

def initialize_reddit():
    reddit = praw.Reddit(client_id = config.client_id,
    client_secret = config.client_secret, user_agent = config.user_agent)
    return reddit

def show_data(input_text, coin):

    if input_text == 'get coin':
        return get_data(coin)

def get_data(coin):
    try:
        web_page = requests.get('https://www.coingecko.com/en/coins/'+coin)
    except:
        return 'error, couldnt find that coin'
    web_page = web_page.content
    soup = BeautifulSoup(web_page, 'html.parser')
    for child in soup.body.children:
        try:
            for i in child.children:
                try:
                    price = i.div.span.text
                    if '$' in price:
                        return price
                except:
                    None
        except:
            None

def format_price(price):
    price = price.split('$')
    price = price[1].replace(',','')
    return price

def get_crypto_comments(subreddit):
    reddit = initialize_reddit()
    hot_post = reddit.subreddit(subreddit).new(limit = 200)
    titles = []
    for post in hot_post:
        if post.score >= 500:
            #print('#-----------------------------------------#------------------------------------#')
            title = post.title.lower()
            titles.append(title)
    return titles

def initialize_twitter():
    
    authenticator = tweepy.OAuthHandler(tk.API_KEY, tk.API_KEY_SECRET)
    authenticator.set_access_token(tk.ACCESS_TOKEN, tk.ACCESSS_TOKEN_SECRET)

    api = tweepy.API(authenticator, wait_on_rate_limit=True)
    
    return api

def search_sentiment(coin:str):

    api = initialize_twitter()

    search = f'#{coin} -filter:retweets'

    tweet_cursor = tweepy.Cursor(api.search_tweets, q=search, lang='en', 
    tweet_mode='extended').items(100)

    tweets = [tweet.full_text for tweet in tweet_cursor]

    tweets_df = pd.DataFrame(tweets, columns=['Tweets'])

    for _, row in tweets_df.iterrows():
        row['Tweets'] = re.sub('http\S+', '', row['Tweets'])
        row['Tweets'] = re.sub('#\S+', '', row['Tweets'])
        row['Tweets'] = re.sub('@\S+', '', row['Tweets'])
        row['Tweets'] = re.sub('\\n', '', row['Tweets'])
    
    tweets_df['Polarity'] = tweets_df['Tweets'].map(lambda tweet: textblob.TextBlob(tweet).sentiment.polarity)

    tweets_df['Result'] = tweets_df['Polarity'].map(lambda pol: '+' if pol > 0 else '-')

    positive = tweets_df[tweets_df.Result == '+'].count()['Tweets']

    negative = tweets_df[tweets_df.Result == '-'].count()['Tweets']

    return positive, negative
    
    # plt.title(coin)
    # plt.bar(['positive', 'negative'], [positive, negative],
    # color=['limegreen', 'red'], edgecolor='black', linewidth=1)
    # plt.xlabel('Sentiment')
    # plt.ylabel('Points')
    # plt.legend()
    # plt.show()
