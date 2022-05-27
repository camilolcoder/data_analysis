import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc, callback
import data_processing as dp
from plotly.subplots import make_subplots
import plotly.graph_objects as go

layout = [
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
                    dbc.Card(children=[
                        dbc.CardBody([
                            dcc.Graph(id='crypto-mc', figure={} ,
                            style = {
                    "overflow":"hidden",
                    "height":"100%",
                    "z-index": 1
                }),
                        ])
                    ]),
                ], width=12),
                ], className = 'mb-2 mt-2'),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='crypto-social', figure={}),
                        ])
                    ]),
                ], width=12),
                ], className = 'mb-2 mt-2'),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='crypto-total-sentiment', figure={}),
                        ])
                    ]),
                    ], width=12),
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

@callback(
        Output('crypto-mc', 'figure'),
        Output('crypto-social', 'figure'),
        Output('crypto-total-sentiment', 'figure'),
        #Output('crypto-trending', 'figure'),
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

    fig.update_yaxes(title_text="<b>Trending values</b>", secondary_y=True)
    fig.update_yaxes(title_text="<b>Crypto price</b>", secondary_y=False, type=scale)

    fig.update_layout(
    font_color="black",
    )

    fig1 = make_subplots(specs=[[{"secondary_y": True}]])#go.Figure()
    df3 = dp.crypto_social_presence(crypto, from_date, to_date) #dp.collect_trend_score('crypto', 1)
    #columns = df1.columns
    #df2 = dp.get_binance_bars('BTCUSDT', '1d', dt.datetime(2020, 1, 1), dt.datetime(2022, 2, 1))
    df4 = dp.crypto_data(crypto, from_date, to_date)

    fig1.add_trace(go.Scatter(x=df3.index, y=df3.value,
                    mode='lines',
                    name='#of followers',
                    line=dict(color='rgb(49,50,58)',
                                width=3)
                    ),secondary_y=True)

    fig1.add_trace(go.Scatter(x=df4.index, y=df4.closePriceUsd,
                    mode='lines',
                    name=crypto+' price',
                    line=dict(color='rgb(51,63,169)',
                                width=3)
                    ),secondary_y=False)
    
    # fig.update_traces(marker_color=['rgb(250,38,52)', 'rgb(65,255,78)'],
    #               marker_line_width=2)

    fig1.update_yaxes(title_text="<b>Social presence</b>", secondary_y=True)
    fig1.update_yaxes(title_text="<b>Crypto price</b>", secondary_y=False)
    
    fig1.update_layout(
    font_color="black",
    )

    fig2 = make_subplots(specs=[[{"secondary_y": True}]])#go.Figure()
    #fig = go.Figure()

    df5 = dp.crypto_positive_sentiment(crypto, from_date, to_date) #dp.collect_trend_score('crypto', 1)
    #columns = df1.columns
    #df2 = dp.get_binance_bars('BTCUSDT', '1d', dt.datetime(2020, 1, 1), dt.datetime(2022, 2, 1))
    df6 = dp.crypto_negative_sentiment(crypto, from_date, to_date)

    df7 = dp.crypto_data(crypto, from_date, to_date)

    fig2.add_trace(go.Scatter(x=df5.index, y=df5.value,
                    mode='lines',
                    name='positive sentiment',
                    line=dict(color='rgb(0,255,128)',
                                width=3)
                    ),secondary_y=True)

    fig2.add_trace(go.Scatter(x=df7.index, y=df7.closePriceUsd,
                    mode='lines',
                    name=crypto+' price',
                    line=dict(color='rgb(0,102,204)',
                                width=3)
                    ),secondary_y=False)

    fig2.add_trace(go.Scatter(x=df6.index, y=df6.value,
                    mode='lines',
                    name=crypto+' negative sentimient',
                    line=dict(color='rgb(255,51,51)',
                                width=3)
                    ),secondary_y=True)
    
    # fig.update_traces(marker_color=['rgb(250,38,52)', 'rgb(65,255,78)'],
    #               marker_line_width=2)

    fig2.update_yaxes(title_text="<b>Social sentiment</b>", secondary_y=True)
    fig2.update_yaxes(title_text="<b>Crypto price</b>", secondary_y=False)
    
    fig2.update_layout(
    font_color="black",
    )

    # fig3 = make_subplots(specs=[[{"secondary_y": True}]])#go.Figure()
    # df8 = dp.collect_trend_score('crypto', 1)
    # columns = df1.columns
    # #df2 = dp.get_binance_bars('BTCUSDT', '1d', dt.datetime(2020, 1, 1), dt.datetime(2022, 2, 1))
    # df9 = dp.crypto_data(crypto, from_date, to_date)

    # fig3.add_trace(go.Scatter(x=df8.index, y=df8[columns[0]],
    #                 mode='lines',
    #                 name='trending',
    #                 line=dict(color='rgb(49,50,58)',
    #                             width=3)
    #                 ),secondary_y=True)

    # fig3.add_trace(go.Scatter(x=df9.index, y=df9.closePriceUsd,
    #                 mode='lines',
    #                 name=crypto+' price',
    #                 line=dict(color='rgb(51,63,169)',
    #                             width=3)
    #                 ),secondary_y=False)
    
    # # fig.update_traces(marker_color=['rgb(250,38,52)', 'rgb(65,255,78)'],
    # #               marker_line_width=2)

    # fig3.update_yaxes(title_text="<b>Trending values</b>", secondary_y=True)
    # fig3.update_yaxes(title_text="<b>Crypto price</b>", secondary_y=False, type='linear')

    # fig3.update_layout(
    # font_color="black",
    # )




    return fig, fig1, fig2 #, figo 