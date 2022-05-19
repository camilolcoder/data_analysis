import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc, callback
import data_processing as dp
import datetime as dt
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from scipy.optimize import curve_fit
import datetime
import pandas_datareader as web


fig = go.Figure()

#df1 = dp.crypto_data('bitcoin', '2011-01-01', '2022-02-02') #dp.collect_trend_score('crypto', 1)
df1 = pd.read_csv('data/BTC_historical_data_clean.csv')
df1 = df1.drop(['Vol.', 'Change %'], axis=1)
df1 = df1.replace(',','', regex=True)
df1.Date = pd.to_datetime(df1.Date)
df1 = df1.set_index('Date')
#print(df)
df1 = df1.apply(pd.to_numeric)
df1.index = df1.index.date
#columns = df1.columns
dff1 = df1.copy()

df_DXY = pd.read_csv('data/DXY_historical_data_clean2.csv')
df_DXY = df_DXY.drop(['Vol.', 'Change %'], axis=1)
df_DXY = df_DXY.replace(',','', regex=True)
df_DXY.Date = pd.to_datetime(df_DXY.Date)
df_DXY = df_DXY.set_index('Date')
#print(df)
df_DXY = df_DXY.apply(pd.to_numeric)
df_DXY.index = df_DXY.index.date


SMA_PERIOD = 20
EMA_PERIOD = 21

df1['sma'] = df1.Price.rolling(window=SMA_PERIOD).mean()
df1['ema'] = df1.Price.ewm(span=EMA_PERIOD,adjust=False).mean()
#dates = len(df1.closePriceUsd)
weeks = np.linspace(1, len(df1), num=len(df1))
btc_price = np.log(df1.Price)

popt, pcov = curve_fit(dp.fitter, weeks, btc_price, p0=(5.0, -15))

fitted_data = dp.fitter(weeks, popt[0], popt[1])


# print(days)
# print(len(days), dates)

coef = np.polyfit(weeks, df1.Price, 1)
equ = np.poly1d(coef)

fig.add_trace(go.Candlestick(x=df1.index, open=df1.Price,
                high=df1.High,
                low=df1.Low,
                close=df1.Price,
                #mode='lines',
                name='BTC price',
                # line=dict(color='rgb(64,64,64)',
                #             width=3)
                ))  

fig.add_trace(go.Scatter(x=df1.index, y=df1.sma,
                mode='lines',
                name='SMA '+str(SMA_PERIOD),
                line=dict(color='rgb(255,51,51)',
                            width=3)
                ))

fig.add_trace(go.Scatter(x=df1.index, y=df1.ema,
                mode='lines',
                name='EMA '+str(EMA_PERIOD),
                line=dict(color='rgb(102,255,102)',
                            width=3)
                ))

# fig.update_traces(marker_color=['rgb(250,38,52)', 'rgb(65,255,78)'],
#               marker_line_width=2)
fig.update_layout(
    title="<b>Bitcoin price (usd) over time</b>",
    # xaxis_title="Date",
    # yaxis_title="Price BTC",
    #legend_title="Legend Title",
    font=dict(
        #family="Courier New, monospace",
        size=13,
        #font_color="black"
        color="black"
    )
    #font_color="black"
)

fig.update_yaxes(title_text="<b>Bitcoin price</b>")
#fig.update_yaxes(title_text="<b>Crypto price</b>", secondary_y=False)

fig.update_layout(
xaxis_rangeslider_visible=False,
template='plotly_dark',
font_color="white",
)

fig1 = go.Figure()

fig1.add_trace(go.Scatter(x=df1.index, y=df1.Price,
                mode='lines',
                name='BTC price',
                line=dict(color='rgb(0,102,204)',
                            width=3)
                ))
for i in range(-2,4):
    fig1.add_trace(go.Scatter(x=df1.index, y=np.exp(fitted_data + i),
                    mode='lines',
                    name='trendline'+str(i),
                    line=dict(color='rgb(49,50,58)',
                                width=3)
                    ))

#fig1.update_xaxes(title_text="<b>Date</b>", type='log', range=[3.3034,3.3057])
fig1.update_layout(
    title="<b>Bitcoin price (usd) over time</b>",
    # xaxis_title="Date",
    # yaxis_title="Price BTC",
    #legend_title="Legend Title",
    font=dict(
        #family="Courier New, monospace",
        size=13,
        #font_color="black"
        color="black"
    )
    #font_color="black"
)

fig1.update_xaxes(title_text="<b>Date</b>")
fig1.update_yaxes(title_text="<b>Price BTC</b>", type='log')#, range=[1.85,5]) #, type='linear'


#df_btc = crypto_data('bitcoin', '2013-01-01', '2022-02-20')
#dff1.index = dff1.index.date
dff1 = dff1.drop(['Open', 'High', 'Low'], axis=1)
start = datetime.datetime(2013, 1, 1)
end = datetime.datetime(2022, 2, 20)
SP500 = web.DataReader(['sp500'], 'fred', start, end)
#print(SP500)

SP500BTC = dff1.merge(SP500, how='inner',
right_index = True, left_index=True)
#print(df_btc)
#print(SP500BTC)

DXY_BTC = dff1.merge(df_DXY, how='inner',
right_index = True, left_index=True)

#print(DXY_BTC)

fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Scatter(x=DXY_BTC.index, y=DXY_BTC.Price_x,
                mode='lines',
                name='BTC price',
                line=dict(color='rgb(0,102,204)',
                            width=3)
                ),secondary_y=True)

fig3.add_trace(go.Scatter(x=DXY_BTC.index, y=DXY_BTC.Price_y,
                mode='lines',
                name='DXY price',
                line=dict(color='rgb(255,51,51)',
                            width=3)
                ),secondary_y=False)

fig3.update_layout(
    title="<b>BTC vs DXY</b>",
    # xaxis_title="Date",
    # yaxis_title="Price BTC",
    #legend_title="Legend Title",
    font=dict(
        #family="Courier New, monospace",
        size=13,
        #font_color="black"
        color="black"
    )
    #font_color="black"
)

fig3.update_xaxes(title_text="<b>Date</b>")
fig3.update_yaxes(title_text="<b>BTC</b>", secondary_y=True, type='log')
fig3.update_yaxes(title_text="<b>DXY</b>", secondary_y=False)

correlation = SP500BTC.corr()
#print(correlation)
#print(correlation)
a = correlation.Price.to_numpy()
b = correlation.sp500.to_numpy()

#print(correlation)

fig2 = px.imshow(correlation, 
        labels = dict(x="<b>Correlation between BTC & S&P500</b>",  color='Correlation'), 
        x=['<b>BTC</b>','<b>S&P500</b>'],
        y=['<b>BTC</b>','<b>S&P500</b>'],  
        color_continuous_scale='RdBu')

fig2.update_layout(
template='plotly_dark',
font_color="white",
)

layout = [
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='bitcoin-main', figure=fig),
                        ])
                    ]),
                ], width=12),]
                , className = 'mb-2 mt-2'),

            #TODO try to get more height for the graph
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='bitcoin-log-log', figure=fig1),
                        ])
                    ]),
                ], width=12),]
                , className = 'mb-2 mt-2'),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='bitcoin-log', figure=fig2),
                        ])
                    ]),
                ], width=6),]
                , className = 'mb-2 mt-2'),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='bitcoin-log', figure=fig3),
                        ])
                    ]),
                ], width=12),]
                , className = 'mb-2 mt-2')

        ]


#######################################
#BITCOIN METRICS
#######################################
# @app.callback(
#         Output('bitcoin-main', 'figure'),
#         # Input('crypto_total_sentiment', 'value'),
#         # Input('from_date_sentiment', 'value'),
#         # Input('to_date_sentiment', 'value'),
# )

# def update_data(): #, year):

#     fig = make_subplots(specs=[[{"secondary_y": True}]])#go.Figure()
#     #fig = go.Figure()

#     df1 = dp.crypto_data('bitcoin', '2013-01-01', '2022-02-02') #dp.collect_trend_score('crypto', 1)
#     #columns = df1.columns
#     #df2 = dp.get_binance_bars('BTCUSDT', '1d', dt.datetime(2020, 1, 1), dt.datetime(2022, 2, 1))
   
#     #df2 = dp.crypto_negative_sentiment(crypto, from_date, to_date)

#     #df3 = dp.crypto_data(crypto, from_date, to_date)

#     fig.add_trace(go.Scatter(x=df1.index, y=df1.value,
#                     mode='lines',
#                     name='positive sentiment',
#                     line=dict(color='rgb(0,255,128)',
#                                 width=3)
#                     ),secondary_y=True)

#     # fig.add_trace(go.Scatter(x=df3.index, y=df3.closePriceUsd,
#     #                 mode='lines',
#     #                 name=crypto+' price',
#     #                 line=dict(color='rgb(0,102,204)',
#     #                             width=3)
#     #                 ),secondary_y=False)

#     # fig.add_trace(go.Scatter(x=df2.index, y=df2.value,
#     #                 mode='lines',
#     #                 name=crypto+' negative sentimient',
#     #                 line=dict(color='rgb(255,51,51)',
#     #                             width=3)
#     #                 ),secondary_y=True)
    
#     # fig.update_traces(marker_color=['rgb(250,38,52)', 'rgb(65,255,78)'],
#     #               marker_line_width=2)

#     fig.update_yaxes(title_text="<b>Social sentiment</b>", secondary_y=True)
#     fig.update_yaxes(title_text="<b>Crypto price</b>", secondary_y=False)
    
#     fig.update_layout(
#     font_color="black",
#     )

#     return fig #, figo
