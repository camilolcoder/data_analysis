import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc, callback
import data_processing as dp
from plotly.subplots import make_subplots
import plotly.graph_objects as go

layout = [
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


@callback(
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