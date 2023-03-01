import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import html, dcc, callback, dash_table
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import data_processing as dp

fig = make_subplots(specs=[[{"secondary_y": True}]])

#DX-Y.NYB

df = dp.get_cross_currencie_data('USDCOP=X', '2011-01-01', '2023-02-20')

df1 = dp.get_cross_currencie_data('DX-Y.NYB', '2011-01-01', '2023-02-20')

fig.add_trace(go.Scatter(x=df.index, y=df.Close,
                mode='lines',
                name='USDCOP',
                line=dict(color='rgb(0,102,204)',
                            width=3)
                ),secondary_y=True)

fig.add_trace(go.Scatter(x=df1.index, y=df1.Close,
                mode='lines',
                name='USD-Index',
                line=dict(color='rgb(0,0,0)',
                            width=3)
                ),secondary_y=False)


layout = [
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='main-currencies', figure=fig),
                        ])
                    ]),
                ], width=12),]
                , className = 'mb-2 mt-2'),

            #TODO try to get more height for the graph
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='bitcoin-log-log', figure={}),
                        ])
                    ]),
                ], width=12),]
                , className = 'mb-2 mt-2'),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='bitcoin-log', figure={}),
                        ])
                    ]),
                ], width=6),]
                , className = 'mb-2 mt-2'),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='bitcoin-log', figure={}),
                        ])
                    ]),
                ], width=12),]
                , className = 'mb-2 mt-2')

        ]

"""
@callback(
    Output('s&p500-i-rates', 'figure'),
        Output('s&p500-print', 'figure'),
        Output('s&p500-res', 'figure')
)

def update_data
"""