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

layout = [
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
                            dcc.Graph(id='s&p500-i-rates', figure={}),
                        ])
                    ]),
                ], width=12),], className = 'mb-2 mt-2'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='s&p500-print', figure={}),
                        ])
                    ]),
                ], width=12),], className = 'mb-2 mt-2'),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='s&p500-res', figure={}),
                        ])
                    ]),
                #],width=6),
                ], width=12),], className = 'mb-2 mt-2'),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Markdown('''
                                #### S&P500 vs US recession

                                This graph shows the performance of the S&P500 and the recessions 
                                it has gone through. The recession data was collected from [FRED](https://fred.stlouisfed.org/)

                                '''),
                        ])
                    ], color='black',  inverse=True),
                ], width=12),], className = 'mb-2 mt-2')
        ]

@callback(
        #Output('s&p500-graph', 'figure'),
        Output('s&p500-i-rates', 'figure'),
        Output('s&p500-print', 'figure'),
        Output('s&p500-res', 'figure'),
        Input('slider-s&p500', 'value'),
        # Input('from_date', 'value'),
        # Input('to_date', 'value'),
)

def update_data(correlation): #, year):
        # s_p500 = yf.Ticker("SPY")
        # s_p500 = s_p500.history(period='max')
        # s_p500 = s_p500.drop(['Open', 'High', 'Low', 
        # 'Volume', 'Dividends', 'Stock Splits'], axis=1)
        # #print(s_p500)
        # s_p500.index = s_p500.index.date
        #df.index = df.index.date
        #print(s_p500)
        s_p500 = pd.read_csv('data/sp500_daily-1950-to-2022.csv')
        #s_p500.index = s_p500.index.date
        s_p500.Date = pd.to_datetime(s_p500.Date)
        s_p500 = s_p500.set_index('Date')
        #print(df)
        s_p500.index = s_p500.index.date

        df = pd.read_csv('data/FEDFUNDS.csv')
        #df = df.rename(columns={'oldName1': 'newName1', 'oldName2': 'newName2'})
        df = df.rename(columns={'DATE':'Date'})
        df.Date = pd.to_datetime(df.Date)
        df = df.set_index('Date')
        #print(df)
        df.index = df.index.date
        #print(df)
        # dff = pd.read_csv('data/WALCL.csv')


        SP500= s_p500.merge(df, how='inner',
                right_index = True, left_index=True)
        
        dff = pd.read_csv('data/WALCL.csv')
        dff = dff.rename(columns={'DATE':'Date'})
        dff.Date = pd.to_datetime(dff.Date)
        dff = dff.set_index('Date')
        #print(df)
        dff.index = dff.index.date

        SP500_P= s_p500.merge(dff, how='inner',
                right_index = True, left_index=True)

        df2 = pd.read_csv('data/USREC.csv')
        df2 = df2.rename(columns={'DATE':'Date'})
        df2.Date = pd.to_datetime(df2.Date)
        df2 = df2.set_index('Date')
        #print(df)
        df2.index = df2.index.date

        SP500_RES= s_p500.merge(df2, how='inner',
                right_index = True, left_index=True)


        #fig1 = go.Figure()
        fig1 = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig1.add_trace(go.Scatter(x=SP500.index, y=SP500.Close,
                        mode='lines',
                        name='S&P500 price',
                        line=dict(color='rgb(64,64,64)',
                                    width=3)
                        ),secondary_y=True)
        
        fig1.add_trace(go.Scatter(x=SP500.index, y=SP500.FEDFUNDS,
                        mode='lines',
                        name='Interest rates',
                        line=dict(color='rgb(255,51,51)',
                                    width=3)
                        ),secondary_y=False)
        
        #fig1.update_xaxes(title_text="<b>Date</b>", type='log', range=[3.3034,3.3057])
        fig1.update_layout(
            title="<b>S&P500 vs Interest rates</b>",
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
        #fig1.update_yaxes(title_text="<b>Price BTC</b>", type='log', range=[1.85,5]) #, type='linear'
        fig1.update_yaxes(title_text="<b>S&P500 price</b>", secondary_y=True, type='log')
        fig1.update_yaxes(title_text="<b>Interest rates</b>", secondary_y=False)

        fig2 = make_subplots(specs=[[{"secondary_y": True}]])

        fig2.add_trace(go.Scatter(x=SP500_P.index, y=SP500_P.Close,
                        mode='lines',
                        name='S&P500 price',
                        line=dict(color='rgb(64,64,64)',
                                    width=3)
                        ),secondary_y=True)
        
        fig2.add_trace(go.Scatter(x=SP500_P.index, y=SP500_P.WALCL,
                        mode='lines',
                        name='Total assets',
                        line=dict(color='rgb(51,255,51)',
                                    width=3)
                        ),secondary_y=False)
        
        #fig1.update_xaxes(title_text="<b>Date</b>", type='log', range=[3.3034,3.3057])
        fig2.update_layout(
            title="<b>S&P500 vs Total assets</b>",
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

        fig2.update_xaxes(title_text="<b>Date</b>")
        #fig1.update_yaxes(title_text="<b>Price BTC</b>", type='log', range=[1.85,5]) #, type='linear'
        fig2.update_yaxes(title_text="<b>S&P500 price</b>", secondary_y=True, type='log')
        fig2.update_yaxes(title_text="<b>Total assets</b>", secondary_y=False)

        fig3 = go.Figure()#make_subplots(specs=[[{"secondary_y": True}]])

        fig3.add_trace(go.Scatter(x=SP500_RES.index, y=SP500_RES.Close,
                        mode='lines',
                        name='S&P500 price',
                        line=dict(color='rgb(64,64,64)',
                                    width=3)
                        ))
        
        recessions = []
        runner = []
        for i, data in enumerate(zip(SP500_RES.index, SP500_RES.USREC)):
            #print(i, data[0], data[1])
            #print(df2.index)
            if data[1] == 1 and SP500_RES.USREC[i-1] == 0:
                runner.append(data[0])
            if data[1] == 0 and SP500_RES.USREC[i-1] == 1:
                runner.append(data[0])
                #print(runner)|
                recessions.append(runner)
                runner = []
        
        for i in range(len(recessions)):

            fig1.add_vrect(
                x0=recessions[i][0], x1=recessions[i][1],
                fillcolor="LightSalmon", opacity=0.5,
                layer="below", line_width=0,
            )

            fig3.add_vrect(
                x0=recessions[i][0], x1=recessions[i][1],
                fillcolor="LightSalmon", opacity=0.5,
                layer="below", line_width=0,
            )

        # fig3.add_vrect(
        #         x0=recessions[2][0], x1=recessions[2][1],
        #         fillcolor="LightSalmon", opacity=0.5,
        #         layer="below", line_width=0,
        #     )

        # print(recessions[2][0], recessions[2][1])
        # print(type(recessions[2][0]), type(recessions[2][1]))
        # fig3.add_trace(go.Scatter(x=SP500_P.index, y=SP500_P.WALCL,
        #                 mode='lines',
        #                 name='Recessions',
        #                 line=dict(color='rgb(51,255,51)',
        #                             width=3)
        #                 ),secondary_y=False)
        
        #fig1.update_xaxes(title_text="<b>Date</b>", type='log', range=[3.3034,3.3057])
        fig3.update_layout(
            title="<b>S&P500 vs US recessions</b>",
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
        #fig1.update_yaxes(title_text="<b>Price BTC</b>", type='log', range=[1.85,5]) #, type='linear'
        fig3.update_yaxes(title_text="<b>S&P500 price</b>", type='log')
        #fig3.update_yaxes(title_text="<b>Recessions</b>", secondary_y=False)

        #DXY_historical_data_clean.csv


        return fig1, fig2, fig3, #fig4 #, figo