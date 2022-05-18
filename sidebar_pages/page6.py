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
                            dcc.Markdown('''

                                ##### What is the Federa Funds Effective Rate?

                                The FFER is the interest rate at which depository institutions trade federal funds with eachother
                                overnight. In simpler terms, a bank with excess cash, which is often referred to as liquidity, 
                                will lend to another bank that needs to quickly raise liquidity. 
                                (1) The rate that the borrowing institution
                                pays to the lending institution is determined between the two banks; the weighted average rate for all of
                                these types of negotiations is called the effective federal funds rate.(2) The effective federal funds 
                                rate is essentially determined by the market but is influenced by the Federal Reserve through open market
                                operations to reach the federal funds rate target.(2) The FFER data was collected 
                                from [FRED](https://fred.stlouisfed.org/)

                                ##### FFER & the S&P500?

                                The reason for showing FFER & the S&P500 its to see the impact the change in interst rates have had over time in 
                                the stock market, interst not only have an impact on the stock market but on the economy as a whole, impacting the 
                                bond markets, inflation, and recessions. more information aboout the impacts of inters rate on the economy can be found
                                on the next article [How interst rates affect the U.S Markets](https://www.investopedia.com/articles/stocks/09/how-interest-rates-affect-markets.asp)


                                '''),
                        ])
                    ], color='dark', outline=True),
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

                                This graph shows the performance of the S&P500 and the recessions 
                                it has gone through. The recession data was collected from [FRED](https://fred.stlouisfed.org/)

                                '''),
                        ])
                    ], color='dark', outline=True),
                ], width=12),], className = 'mb-2 mt-2'),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='s&p500-rsxfs', figure={}),
                        ])
                    ]),
                #],width=6),
                ], width=12),], className = 'mb-2 mt-2'),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Markdown('''

                                This graph shows the performance of the S&P500 and the historical retail
                                sales in millions of dollars. The historical retail data was collected 
                                from [FRED](https://fred.stlouisfed.org/)

                                '''),
                        ])
                    ], color='dark',  outline=True),
                ], width=12),], className = 'mb-2 mt-2')
        ]

@callback(
        Output('s&p500-i-rates', 'figure'),
        Output('s&p500-print', 'figure'),
        Output('s&p500-res', 'figure'),
        Output('s&p500-rsxfs', 'figure'),
        Input('slider-s&p500', 'value'),
)

def update_data(correlation):

        #S&P500 Historical data
        s_p500 = pd.read_csv('data/sp500_daily-1950-to-2022.csv')
        s_p500.Date = pd.to_datetime(s_p500.Date)
        s_p500 = s_p500.set_index('Date')
        s_p500.index = s_p500.index.date
        
        #US interest rates Historical data
        df = pd.read_csv('data/FEDFUNDS.csv')
        df = df.rename(columns={'DATE':'Date'})
        df.Date = pd.to_datetime(df.Date)
        df = df.set_index('Date')
        df.index = df.index.date

        SP500= s_p500.merge(df, how='inner',
                right_index = True, left_index=True)
        
        #US total assets Historical data
        dff = pd.read_csv('data/WALCL.csv')
        dff = dff.rename(columns={'DATE':'Date'})
        dff.Date = pd.to_datetime(dff.Date)
        dff = dff.set_index('Date')
        dff.index = dff.index.date

        SP500_P= s_p500.merge(dff, how='inner',
                right_index = True, left_index=True)

        #US recessions Historical data
        df2 = pd.read_csv('data/USREC.csv')
        df2 = df2.rename(columns={'DATE':'Date'})
        df2.Date = pd.to_datetime(df2.Date)
        df2 = df2.set_index('Date')
        df2.index = df2.index.date

        SP500_RES= s_p500.merge(df2, how='inner',
                right_index = True, left_index=True)

        #US Advance retail sales Historical data
        df3 = pd.read_csv('data/RSXFS.csv')
        df3 = df3.rename(columns={'DATE':'Date'})
        df3.Date = pd.to_datetime(df3.Date)
        df3 = df3.set_index('Date')
        df3.index = df3.index.date

        SP500_CPI = s_p500.merge(df3, how='inner',
                right_index = True, left_index=True)

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
            title="<b>S&P500 & Interest rates</b>",
            font=dict(
                size=13,
                color="black"
            )
        )

        fig1.update_xaxes(title_text="<b>Date</b>")
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
        
        fig2.update_layout(
            title="<b>S&P500 & Total assets</b>",
            font=dict(
                size=13,
                color="black"
            )
        )

        fig2.update_xaxes(title_text="<b>Date</b>")
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

        # print(recessions[2][0], recessions[2][1])
        # print(type(recessions[2][0]), type(recessions[2][1]))
        # fig3.add_trace(go.Scatter(x=SP500_P.index, y=SP500_P.WALCL,
        #                 mode='lines',
        #                 name='Recessions',
        #                 line=dict(color='rgb(51,255,51)',
        #                             width=3)
        #                 ),secondary_y=False)
        
        fig3.update_layout(
            title="<b>S&P500 & US recessions</b>",
            font=dict(
                size=13,
                color="black"
            )
        )

        fig3.update_xaxes(title_text="<b>Date</b>")
        #fig1.update_yaxes(title_text="<b>Price BTC</b>", type='log', range=[1.85,5]) #, type='linear'
        fig3.update_yaxes(title_text="<b>S&P500 price</b>", type='log')
        #fig3.update_yaxes(title_text="<b>Recessions</b>", secondary_y=False)

        fig4 = make_subplots(specs=[[{"secondary_y": True}]])

        fig4.add_trace(go.Scatter(x=SP500_CPI.index, y=SP500_CPI.Close,
                        mode='lines',
                        name='S&P500 price',
                        line=dict(color='rgb(64,64,64)',
                                    width=3)
                        ),secondary_y=True)
        
        fig4.add_trace(go.Scatter(x=SP500_CPI.index, y=SP500_CPI.RSXFS,
                        mode='lines',
                        name='ARS',
                        line=dict(color='rgb(51,255,51)',
                                    width=3)
                        ),secondary_y=False)
        
        fig4.update_layout(
            title="<b>S&P500 & Advance retail sales</b>",
            font=dict(
                size=13,
                color="black"
            )
        )

        fig4.update_yaxes(title_text="<b>S&P500 price</b>", secondary_y=True, type='log')
        fig4.update_xaxes(title_text="<b>Date</b>")
        fig4.update_yaxes(title_text="<b>ARS Millions of Dollars</b>", secondary_y=False, type='log')


        return fig1, fig2, fig3, fig4 #, figo