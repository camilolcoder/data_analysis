import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc, callback, html, dash_table
import data_processing as dp
from plotly.subplots import make_subplots
import plotly.graph_objects as go

economic_df = dp.economic_calendar()
economic_df = economic_df.drop(['id'], axis=1)

colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    'main_color': '#000000'
}

layout = [
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            # dcc.Graph(id='economic-calendar', figure={}),
                            html.H2(children='Economic calendar',
                                    style={
                                        'textAlign':'center',
                                        'color': colors['main_color']
                                    }),
                            dash_table.DataTable(
                                # data = dict(values=[economic_df.id, economic_df.date, economic_df.time
                                #       , economic_df.zone, economic_df.currency, economic_df.importance, economic_df.event,
                                #       economic_df.actual, economic_df.forecast, economic_df.previous]),
                                data = economic_df.to_dict('records'),
                                columns =[{'id': c, 'name':c} for c in economic_df.columns],
                                page_size=15,
                                style_table={'height':'350px', 'overflowY':'auto'},
                                style_data={
                                    'color': 'black',
                                    'backgroundColor': 'white',
                                    'border': '1px solid black'
                                },
                                style_data_conditional=[
                                    {
                                        'if': {
                                            'filter_query': '{importance} = low',
                                            'column_id': 'importance'
                                        },
                                        'backgroundColor': 'rgb(153, 255, 51)',
                                        'color': 'black'
                                    },
                                    {
                                        'if': {
                                            'filter_query': '{importance} = medium',
                                            'column_id': 'importance'
                                        },
                                        'backgroundColor': 'rgb(255, 255, 51)',
                                        'color': 'black'
                                    },
                                    {
                                        'if': {
                                            'filter_query': '{importance} = high',
                                            'column_id': 'importance'
                                        },
                                        'backgroundColor': 'rgb(255, 51, 51)',
                                        'color': 'black'
                                    }
                                ],
                                style_header={
                                    'backgroundColor': 'rgb(210, 210, 210)',
                                    'color': 'black',
                                    'fontWeight': 'bold',
                                    'border': '1px solid black',
                                    'textAlign': 'center'
                                }    
                            )
                        ])
                    ]),
                #],width=6),
                ], width=12),], className = 'mb-2 mt-2'),
        ]

# layout = [
#             dbc.Row([
#                 dbc.Col([
#                     dcc.Input(
#                         id = 'crypto_name',
#                         placeholder='Enter a crypto...',
#                         type='text',
#                         value='bitcoin',
#                         style={'width':'100%'},
#                     )
#                 ], width=6),
#                 dbc.Col([
#                     dcc.Input(
#                         id = 'from_date',
#                         placeholder='Enter a crypto...',
#                         type='text',
#                         value='2017-01-01',
#                         style={'width':'100%'},
#                     )
#                 ], width=3),
#                 dbc.Col([
#                     dcc.Input(
#                         id = 'to_date',
#                         placeholder='Enter a crypto...',
#                         type='text',
#                         value='2022-02-02',
#                         style={'width':'100%'},
#                     )
#                 ], width=3),
#                 ], className = 'mb-2 mt-2'),
#             dbc.Row([
#                 dbc.Col([
#                     dbc.Card([
#                         dbc.CardBody([
#                             dcc.Graph(id='crypto-trending', figure={}),
#                         ])
#                     ]),
#                 ], width=12),
#                 ], className = 'mb-2 mt-2')
#         ]


# @callback(
#         Output('crypto-trending', 'figure'),
#         Input('crypto_name', 'value'),
#         Input('from_date', 'value'),
#         Input('to_date', 'value'),
# )

# def update_data(crypto, from_date, to_date): #, year):

#     fig = make_subplots(specs=[[{"secondary_y": True}]])#go.Figure()
#     df1 = dp.collect_trend_score('crypto', 1)
#     columns = df1.columns
#     #df2 = dp.get_binance_bars('BTCUSDT', '1d', dt.datetime(2020, 1, 1), dt.datetime(2022, 2, 1))
#     df2 = dp.crypto_data(crypto, from_date, to_date)

#     fig.add_trace(go.Scatter(x=df1.index, y=df1[columns[0]],
#                     mode='lines',
#                     name='trending',
#                     line=dict(color='rgb(49,50,58)',
#                                 width=3)
#                     ),secondary_y=True)

#     fig.add_trace(go.Scatter(x=df2.index, y=df2.closePriceUsd,
#                     mode='lines',
#                     name=crypto+' price',
#                     line=dict(color='rgb(51,63,169)',
#                                 width=3)
#                     ),secondary_y=False)
    
#     # fig.update_traces(marker_color=['rgb(250,38,52)', 'rgb(65,255,78)'],
#     #               marker_line_width=2)

#     fig.update_yaxes(title_text="<b>Trending values</b>", secondary_y=True)
#     fig.update_yaxes(title_text="<b>Crypto price</b>", secondary_y=False, type='linear')

#     fig.update_layout(
#     font_color="black",
#     )

#     return fig #, figo