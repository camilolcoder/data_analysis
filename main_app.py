# Code source: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
#import dash_core_components as dcc
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go

import data_processing as dp
import datetime as dt
import pandas as pd
import numpy as np
#from scipy.optimize import curve_fit

import datetime
import pandas_datareader as web
from plotly.subplots import make_subplots

import networkx as nx
import math

# data source: https://www.kaggle.com/chubak/iranian-students-from-1968-to-2017
# data owner: Chubak Bidpaa
#df = pd.read_csv('https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Bootstrap/Side-Bar/iranian_students.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#47627d",
    "overflow":"scroll",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

NAVBAR_STYLE = {
    "color": "#fff",
    "font-size": "16px",
    #"font-weight": 700,
    #"background-color": "#bedbf7",
}

sidebar = html.Div(
    [
        html.H2("Beta 1.0 metrics", className="display-4"),
        html.Hr(),
        html.P(
            "Metrics for analysis", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Crypto price vs trending", href="/", active="exact", style=NAVBAR_STYLE),
                dbc.NavLink("Crypto price vs mc", href="/page-1", active="exact", style=NAVBAR_STYLE),
                dbc.NavLink("Crypto adresses growth", href="/page-2", active="exact", style=NAVBAR_STYLE),
                dbc.NavLink("Crypto twitter growth", href="/page-3", active="exact", style=NAVBAR_STYLE),
                dbc.NavLink("Crypto total sentiment", href="/page-4", active="exact", style=NAVBAR_STYLE),
                dbc.NavLink('Bitcoin analysis metrics', href="/page-5", active="exact", style=NAVBAR_STYLE),
                dbc.NavLink('S&P 500 metrics', href="/page-6", active="exact", style=NAVBAR_STYLE),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    # figo = go.Figure(go.Bar(x=['positive', 'negative'],y=[43 , 67]))

    # figo.update_traces(marker_color=['rgb(250,38,52)', 'rgb(65,255,78)'], marker_line_color='rgb(0,0,0)',
    #               marker_line_width=2, opacity=0.6)
    # #figo = px.bar([['positive', 'negative'],[positive , negative]], x='sentiment', y='pop')
    # #title="Plot Title",

    # figo.update_layout(
    # xaxis_title="<b>Bitcoin sentiment</b>",
    # yaxis_title="<b>Sentiment points</b>",
    # legend_title="Legend Title",
    # font=dict(
    #     family="Courier New, monospace",
    #     size=18,
    #     color="Black" 
    # ))

    if pathname == "/":
        return [
                dbc.Row([
                    dbc.Col([
                        dcc.Input(
                            id = 'crypto_name',
                            placeholder='Enter a crypto...',
                            type='text',
                            value='bitcoin',
                            style={'width':'100%'},
                        )
                    ], width=6),
                    dbc.Col([
                        dcc.Input(
                            id = 'from_date',
                            placeholder='Enter a crypto...',
                            type='text',
                            value='2017-01-01',
                            style={'width':'100%'},
                        )
                    ], width=3),
                    dbc.Col([
                        dcc.Input(
                            id = 'to_date',
                            placeholder='Enter a crypto...',
                            type='text',
                            value='2022-02-02',
                            style={'width':'100%'},
                        )
                    ], width=3),
                    ], className = 'mb-2 mt-2'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='crypto-trending', figure={}),
                            ])
                        ]),
                    ], width=12),
                    ], className = 'mb-2 mt-2')
                ]
    elif pathname == "/page-1":
        return [
                # html.H1('Crypto sentiment',
                #         style={'textAlign':'center'}),
                # dcc.Graph(id='bargraph',
                #          figure={})

                dbc.Row([
                    dbc.Col([
                        dcc.Input(
                            id = 'crypto_name_mc',
                            placeholder='Enter a crypto...',
                            type='text',
                            value='bitcoin',
                            style={'width':'100%'},
                        )
                    ], width=3),
                     dbc.Col([
                        dcc.Dropdown(id='slc_scale',
                                options = [
                                    {'label':'linear scale', 'value': 'linear'},
                                    {'label':'logarithmic scale', 'value':'log'}
                                ],
                                multi = False,
                                value = 'linear',
                                style={'width':'100%'},
                        )
                    ], width=3),        
                    dbc.Col([
                        dcc.Input(
                            id = 'from_date_mc',
                            placeholder='Enter a crypto...',
                            type='text',
                            value='2017-01-01',
                            style={'width':'100%'},
                        )
                    ], width=3),
                    dbc.Col([
                        dcc.Input(
                            id = 'to_date_mc',
                            placeholder='Enter a crypto...',
                            type='text',
                            value='2022-02-02',
                            style={'width':'100%'},
                        )
                    ], width=3),
                    ], className = 'mb-2 mt-2'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='crypto-mc', figure={}),
                            ])
                        ]),
                    ], width=12),
                    ], className = 'mb-2 mt-2')

                ]
    elif pathname == "/page-2":
        return [
              
                dbc.Row([
                    dbc.Col([
                        dcc.Input(
                            id = 'crypto_name_growth',
                            placeholder='Enter a crypto...',
                            type='text',
                            value='bitcoin',
                            style={'width':'100%'},
                        )
                    ], width=6),
                    dbc.Col([
                        dcc.Input(
                            id = 'from_date_growth',
                            placeholder='Enter a crypto...',
                            type='text',
                            value='2017-01-01',
                            style={'width':'100%'},
                        )
                    ], width=3),
                    dbc.Col([
                        dcc.Input(
                            id = 'to_date_growth',
                            placeholder='Enter a crypto...',
                            type='text',
                            value='2022-02-02',
                            style={'width':'100%'},
                        )
                    ], width=3),
                    ], className = 'mb-2 mt-2'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='crypto-growth', figure={}),
                            ])
                        ]),
                    ], width=12),
                    ], className = 'mb-2 mt-2')

                ]

    elif pathname == "/page-3":
        return [
                dbc.Row([
                    dbc.Col([
                        dcc.Input(
                            id = 'crypto_name_social',
                            placeholder='Enter a crypto...',
                            type='text',
                            value='bitcoin',
                            style={'width':'100%'},
                        )
                    ], width=6),
                    dbc.Col([
                        dcc.Input(
                            id = 'from_date_social',
                            placeholder='Enter a crypto...',
                            type='text',
                            value='2017-01-01',
                            style={'width':'100%'},
                        )
                    ], width=3),
                    dbc.Col([
                        dcc.Input(
                            id = 'to_date_social',
                            placeholder='Enter a crypto...',
                            type='text',
                            value='2022-02-02',
                            style={'width':'100%'},
                        )
                    ], width=3),
                    ], className = 'mb-2 mt-2'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='crypto-social', figure={}),
                            ])
                        ]),
                    ], width=12),
                    ], className = 'mb-2 mt-2')

                ]
    elif pathname == "/page-4":
        return [
                dbc.Row([
                    dbc.Col([
                        dcc.Input(
                            id = 'crypto_total_sentiment',
                            placeholder='Enter a crypto...',
                            type='text',
                            value='bitcoin',
                            style={'width':'100%'},
                        )
                    ], width=6),
                    dbc.Col([
                        dcc.Input(
                            id = 'from_date_sentiment',
                            placeholder='Enter a crypto...',
                            type='text',
                            value='2017-01-01',
                            style={'width':'100%'},
                        )
                    ], width=3),
                    dbc.Col([
                        dcc.Input(
                            id = 'to_date_sentiment',
                            placeholder='Enter a crypto...',
                            type='text',
                            value='2022-02-02',
                            style={'width':'100%'},
                        )
                    ], width=3),
                    ], className = 'mb-2 mt-2'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='crypto-total-sentiment', figure={}),
                            ])
                        ]),
                    ], width=12),
                    ], className = 'mb-2 mt-2')

                ]
    elif pathname == "/page-5":
        #fig = make_subplots(specs=[[{"secondary_y": True}]])#go.Figure()
        fig = go.Figure()

        df1 = dp.crypto_data('bitcoin', '2011-01-01', '2022-02-02') #dp.collect_trend_score('crypto', 1)
        #columns = df1.columns
        dff1 = df1.copy()

        SMA_PERIOD = 20
        EMA_PERIOD = 21

        df1['sma'] = df1.closePriceUsd.rolling(window=SMA_PERIOD).mean()
        df1['ema'] = df1.closePriceUsd.ewm(span=EMA_PERIOD,adjust=False).mean()
        #dates = len(df1.closePriceUsd)
        days = np.linspace(1, len(df1), num=len(df1))
        btc_price = np.log(df1.closePriceUsd)

        #popt, pcov = curve_fit(dp.fitter, days, btc_price, p0=(5.0, -15))

        #fitted_data = dp.fitter(days, popt[0], popt[1])


        # print(days)
        # print(len(days), dates)

        # coef = np.polyfit(days, df1.closePriceUsd, 1)
        # equ = np.poly1d(coef)

        fig.add_trace(go.Candlestick(x=df1.index, open=df1.openPriceUsd,
                        high=df1.highPriceUsd,
                        low=df1.lowPriceUsd,
                        close=df1.closePriceUsd,
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
        
        fig1.add_trace(go.Scatter(x=df1.index, y=df1.closePriceUsd,
                        mode='lines',
                        name='BTC price',
                        line=dict(color='rgb(0,102,204)',
                                    width=3)
                        ))
        # for i in range(-2,4):
        #     fig1.add_trace(go.Scatter(x=df1.index, y=np.exp(fitted_data + i),
        #                     mode='lines',
        #                     name='trendline'+str(i),
        #                     line=dict(color='rgb(49,50,58)',
        #                                 width=3)
        #                     ))
        
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
        fig1.update_yaxes(title_text="<b>Price BTC</b>", type='log', range=[1.85,5]) #, type='linear'
        
        # fig1.update_layout(
        # font_color="black",
        # )

        #df_btc = crypto_data('bitcoin', '2013-01-01', '2022-02-20')
        dff1.index = dff1.index.date
        dff1 = dff1.drop(['openPriceUsd', 'highPriceUsd', 'lowPriceUsd', 'volume', 'marketcap'], axis=1)
        start = datetime.datetime(2013, 1, 1)
        end = datetime.datetime(2022, 2, 20)
        SP500 = web.DataReader(['sp500'], 'fred', start, end)
        #print(SP500)

        SP500BTC = dff1.merge(SP500, how='inner',
        right_index = True, left_index=True)
        #print(df_btc)
        #print(SP500BTC)

        correlation = SP500BTC.corr()
        #print(correlation)
        a = correlation.closePriceUsd.to_numpy()
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

        return [
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
                    , className = 'mb-2 mt-2')

        ]

    elif pathname == "/page-6":
        return [
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Slider(0, 1, 0.05,
                                value=0.50,
                                id='slider-s&p500',
                                ),
                            ])
                        ]),
                    ], width=12),]
                    , className = 'mb-2 mt-2'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='s&p500-graph', figure={}),
                            ])
                        ]),
                    ], width=12),], className = 'mb-2 mt-2')
        ]
        
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

#######################################
#CRYPTO TRENDING
#######################################
@app.callback(
        Output('crypto-trending', 'figure'),
        Input('crypto_name', 'value'),
        Input('from_date', 'value'),
        Input('to_date', 'value'),
)

def update_data(crypto, from_date, to_date): #, year):

    fig = make_subplots(specs=[[{"secondary_y": True}]])#go.Figure()
    df1 = dp.collect_trend_score('crypto', 1)
    columns = df1.columns
    #df2 = dp.get_binance_bars('BTCUSDT', '1d', dt.datetime(2020, 1, 1), dt.datetime(2022, 2, 1))
    df2 = dp.crypto_data(crypto, from_date, to_date)

    fig.add_trace(go.Scatter(x=df1.index, y=df1[columns[0]],
                    mode='lines',
                    name='trending',
                    line=dict(color='rgb(49,50,58)',
                                width=3)
                    ),secondary_y=True)

    fig.add_trace(go.Scatter(x=df2.index, y=df2.closePriceUsd,
                    mode='lines',
                    name=crypto+' price',
                    line=dict(color='rgb(51,63,169)',
                                width=3)
                    ),secondary_y=False)
    
    # fig.update_traces(marker_color=['rgb(250,38,52)', 'rgb(65,255,78)'],
    #               marker_line_width=2)

    fig.update_yaxes(title_text="<b>Trending values</b>", secondary_y=True)
    fig.update_yaxes(title_text="<b>Crypto price</b>", secondary_y=False, type='linear')

    fig.update_layout(
    font_color="black",
    )

    return fig #, figo


#######################################
#CRYPTO PRICE VS MARKETCAP
#######################################
@app.callback(
        Output('crypto-mc', 'figure'),
        Input('crypto_name_mc', 'value'),
        Input('slc_scale', 'value'),
        Input('from_date_mc', 'value'),
        Input('to_date_mc', 'value'),
)

def update_data(crypto, scale, from_date, to_date): #, year):

    fig = make_subplots(specs=[[{"secondary_y": True}]])#go.Figure()
    df1 = dp.market_cap(crypto, from_date, to_date)
    columns = df1.columns
    #df2 = dp.get_binance_bars('BTCUSDT', '1d', dt.datetime(2020, 1, 1), dt.datetime(2022, 2, 1))
    df2 = dp.crypto_data(crypto, from_date, to_date)

    fig.add_trace(go.Scatter(x=df1.index, y=df1[columns[0]],
                    mode='lines',
                    name='trending',
                    line=dict(color='rgb(49,50,58)',
                                width=3)
                    ),secondary_y=True)

    fig.add_trace(go.Scatter(x=df2.index, y=df2.closePriceUsd,
                    mode='lines',
                    name=crypto+' price',
                    line=dict(color='rgb(51,63,169)',
                                width=3)
                    ),secondary_y=False)
    
    # fig.update_traces(marker_color=['rgb(250,38,52)', 'rgb(65,255,78)'],
    #               marker_line_width=2)

    fig.update_yaxes(title_text="<b>Trending values</b>", secondary_y=True)
    fig.update_yaxes(title_text="<b>Crypto price</b>", secondary_y=False, type=scale)

    fig.update_layout(
    font_color="black",
    )

    return fig #, figo

#######################################
#GROWTH WITH ADRESSES
#######################################
@app.callback(
        Output('crypto-growth', 'figure'),
        Input('crypto_name_growth', 'value'),
        Input('from_date_growth', 'value'),
        Input('to_date_growth', 'value'),
)

def update_data(crypto, from_date, to_date): #, year):

    fig = make_subplots(specs=[[{"secondary_y": True}]])#go.Figure()
    df1 = dp.crypto_growth(crypto, from_date, to_date) #dp.collect_trend_score('crypto', 1)
    #columns = df1.columns
    #df2 = dp.get_binance_bars('BTCUSDT', '1d', dt.datetime(2020, 1, 1), dt.datetime(2022, 2, 1))
    df2 = dp.crypto_data(crypto, from_date, to_date)

    fig.add_trace(go.Scatter(x=df1.index, y=df1.value,
                    mode='lines',
                    name='#wallets',
                    line=dict(color='rgb(49,50,58)',
                                width=3)
                    ),secondary_y=True)

    fig.add_trace(go.Scatter(x=df2.index, y=df2.closePriceUsd,
                    mode='lines',
                    name=crypto+' price',
                    line=dict(color='rgb(51,63,169)',
                                width=3)
                    ),secondary_y=False)
    
    # fig.update_traces(marker_color=['rgb(250,38,52)', 'rgb(65,255,78)'],
    #               marker_line_width=2)

    fig.update_yaxes(title_text="<b>Crypto price</b>", secondary_y=True)
    fig.update_yaxes(title_text="<b>Trending values</b>", secondary_y=False)

    fig.update_layout(
    font_color="black",
    )

    return fig #, figo

#######################################
#SOCIAl PRESENCE 
#######################################
@app.callback(
        Output('crypto-social', 'figure'),
        Input('crypto_name_social', 'value'),
        Input('from_date_social', 'value'),
        Input('to_date_social', 'value'),
)

def update_data(crypto, from_date, to_date): #, year):

    fig = make_subplots(specs=[[{"secondary_y": True}]])#go.Figure()
    df1 = dp.crypto_social_presence(crypto, from_date, to_date) #dp.collect_trend_score('crypto', 1)
    #columns = df1.columns
    #df2 = dp.get_binance_bars('BTCUSDT', '1d', dt.datetime(2020, 1, 1), dt.datetime(2022, 2, 1))
    df2 = dp.crypto_data(crypto, from_date, to_date)

    fig.add_trace(go.Scatter(x=df1.index, y=df1.value,
                    mode='lines',
                    name='#of followers',
                    line=dict(color='rgb(49,50,58)',
                                width=3)
                    ),secondary_y=True)

    fig.add_trace(go.Scatter(x=df2.index, y=df2.closePriceUsd,
                    mode='lines',
                    name=crypto+' price',
                    line=dict(color='rgb(51,63,169)',
                                width=3)
                    ),secondary_y=False)
    
    # fig.update_traces(marker_color=['rgb(250,38,52)', 'rgb(65,255,78)'],
    #               marker_line_width=2)

    fig.update_yaxes(title_text="<b>Social presence</b>", secondary_y=True)
    fig.update_yaxes(title_text="<b>Crypto price</b>", secondary_y=False)
    
    fig.update_layout(
    font_color="black",
    )

    return fig #, figo

#######################################
#TOTAL SENTIMENT
#######################################
@app.callback(
        Output('crypto-total-sentiment', 'figure'),
        Input('crypto_total_sentiment', 'value'),
        Input('from_date_sentiment', 'value'),
        Input('to_date_sentiment', 'value'),
)

def update_data(crypto, from_date, to_date): #, year):

    fig = make_subplots(specs=[[{"secondary_y": True}]])#go.Figure()
    #fig = go.Figure()

    df1 = dp.crypto_positive_sentiment(crypto, from_date, to_date) #dp.collect_trend_score('crypto', 1)
    #columns = df1.columns
    #df2 = dp.get_binance_bars('BTCUSDT', '1d', dt.datetime(2020, 1, 1), dt.datetime(2022, 2, 1))
    df2 = dp.crypto_negative_sentiment(crypto, from_date, to_date)

    df3 = dp.crypto_data(crypto, from_date, to_date)

    fig.add_trace(go.Scatter(x=df1.index, y=df1.value,
                    mode='lines',
                    name='positive sentiment',
                    line=dict(color='rgb(0,255,128)',
                                width=3)
                    ),secondary_y=True)

    fig.add_trace(go.Scatter(x=df3.index, y=df3.closePriceUsd,
                    mode='lines',
                    name=crypto+' price',
                    line=dict(color='rgb(0,102,204)',
                                width=3)
                    ),secondary_y=False)

    fig.add_trace(go.Scatter(x=df2.index, y=df2.value,
                    mode='lines',
                    name=crypto+' negative sentimient',
                    line=dict(color='rgb(255,51,51)',
                                width=3)
                    ),secondary_y=True)
    
    # fig.update_traces(marker_color=['rgb(250,38,52)', 'rgb(65,255,78)'],
    #               marker_line_width=2)

    fig.update_yaxes(title_text="<b>Social sentiment</b>", secondary_y=True)
    fig.update_yaxes(title_text="<b>Crypto price</b>", secondary_y=False)
    
    fig.update_layout(
    font_color="black",
    )

    return fig #, figo


#######################################
#S&P500 TRENDING
#######################################
@app.callback(
        Output('s&p500-graph', 'figure'),
        Input('slider-s&p500', 'value'),
        # Input('from_date', 'value'),
        # Input('to_date', 'value'),
)

def update_data(correlation): #, year):

    network = go.Figure(data=[go.Scatter(x=[], y=[], mode='lines', text=[],  line=dict(color='MediumPurple',width=10),
                                           marker=dict(size=20, line_width=10,line=dict(color='MediumPurple',width=2))),
                                go.Scatter(x=[], y=[],mode='markers+text', textposition="top center", 
                                          text=[],hoverinfo='text',textfont_size=12, marker=dict(size=50, color=[],line_width=1))],
                          layout=go.Layout( showlegend=False, annotations=[], margin=dict(t=40, b=0, l=0, r=0)))#, width=1600, height=800))

    payload = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    sp500_table = payload[0]
    sp500_table

    sp500_names = sp500_table.Security.values
    sp500_tickers = sp500_table.Symbol.str.upper().values
    sp500_sectors = sp500_table["GICS Sector"].values
    sp500_sub_sectors = sp500_table["GICS Sub-Industry"].values

    # sp500_names_mapping = dict(zip(sp500_tickers, sp500_names))
    # sp500_sector_mapping = dict(zip(sp500_names, sp500_sectors))
    # sp500_sub_sector_mapping = dict(zip(sp500_names, sp500_sub_sectors))
    # sector_color_mapping = dict(zip(sp500_sectors, sns.color_palette("pastel", len(sp500_sectors)).as_hex()))
    # subsector_color_mapping = dict(zip(sp500_sub_sectors, sns.color_palette("pastel", len(sp500_sub_sectors)).as_hex()))        

    dff = pd.read_csv('data/sp500_corr_data.csv')
    threshold, corr_mode = None, None
    threshold = correlation

    corr_matrix = dff.to_numpy()
    
    G = nx.from_numpy_matrix(corr_matrix)
    G = nx.relabel_nodes(G, lambda x: dff.columns.tolist()[x])

    remove = []

    for col1, col2, weight in G.edges(data=True):

        if math.isnan(weight["weight"]):
            remove.append((col1,col2))
    
        if abs(weight["weight"]) < threshold:
            remove.append((col1,col2))
    
    G.remove_edges_from(remove)
    
    remove = []
    edges = list(sum(G.edges, ()))

    for node in G.nodes:
        if node not in edges:
            remove.append(node)

    G.remove_nodes_from(remove)
    mst = nx.maximum_spanning_tree(G)

    labels = {n:n for n in mst.nodes()}
    node_x = []
    node_y = []

    tree = nx.fruchterman_reingold_layout(mst, k=0.25).items()

    for node, (x_,y_) in tree:
        node_x.append(x_)
        node_y.append(y_)
        
    def get_dim_of_node(name):
        for node, (x,y) in tree:
            if node == name:
                return x,y
        
    edge_x = []
    edge_y = []
    
    weights= []
    for node1, node2, w in mst.edges(data=True):
        x0, y0 = get_dim_of_node(node1)
        x1, y1 =  get_dim_of_node(node2)
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
        weights.append((round(w["weight"],1), (x0+x1)/2, (y0+y1)/2))
    # annotations_list =[dict(x=weight[1], y=weight[2], xref='x', yref='y', text=weight[0], ax=weight[1], ay=weight[2]) for weight in weights]
                              
    with network.batch_update():
        network.data[1].x = node_x
        network.data[1].y = node_y
        network.data[1].text = list(labels)
        #network.data[1].marker.color = node_colors
        # network.update_layout(annotations=annotations_list)
                          
        network.data[0].x = edge_x
        network.data[0].y = edge_y
        network.data[0].text = list(weights)
        network.update_layout(xaxis_zeroline=False, yaxis_zeroline=False, xaxis_showgrid=False, yaxis_showgrid=False, plot_bgcolor='rgba(0,0,0,0)')


    #fig = go.figure()

    return network #, figo

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

#DONE implement bootstrap for all of the pages and implement new metrics
#DONE implement logarithmic scale options
#TODO implement new metrics section for total crypto asset class

if __name__=='__main__':
    app.run_server(debug=True)#, port=3000)
