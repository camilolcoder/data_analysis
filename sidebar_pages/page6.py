import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import html, dcc, callback, dash_table
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import data_processing as dp

# economic_df = dp.economic_calendar()
# economic_df = economic_df.drop(['id'], axis=1)

# CONTENT_STYLE = {
#     #"margin-left": "18rem",
#     #"margin-right": "2rem",
#     #"padding": "2rem 1rem",
#     "padding-top": "55px",
#     "overflow":"scroll",
#     "z-index":1
#     }

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
                            dcc.Markdown('''

                                The red rectangles in the back of the graphs means a period of recession. 
                                The recession data was collected from [FRED](https://fred.stlouisfed.org/)

                                '''),
                        ])
                    ], color='danger', inverse=True),
                ], width=12),], className = 'mb-2 mt-2'),

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

                                The reason for showing FFER & the S&P500 its to see the impact the change in interest rates has had in 
                                the stock market over time, interest not only have an impact on the stock market but on the economy as a whole, influencing the 
                                bond markets, inflation, and recessions. More information aboout the impacts of inters rate on the economy can be found
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
                            dcc.Markdown('''
                                
                                ##### The Fed's Balance Sheet
                                
                                All of us are connected to the Fed's balance sheet in one way or another. The currency notes
                                that we hold are liabilities of the Fed, as are bank reserves boosted by our deposits. The Fed's 
                                assets include a range of credit lines established to ensure the economy's stability at times of crisis,
                                as well as U.S. Treasuries we also hold in investment portfolios. Changes in the level and composition of
                                the Fed's balance sheet can ultimately affect all U.S. consumers and businesses. 
                                The total assets data was collected from [FRED](https://fred.stlouisfed.org/)
                                More information about the federal reserve balance sheet can be found 
                                on [Understanding the federal Reserve Balance Sheet](https://www.investopedia.com/articles/economics/10/understanding-the-fed-balance-sheet.asp)
                                
                                In the graph we can notice some periods of QE(Quantitaive easing) or large scale asset purchases,
                                this is intended to signal the central bank's bias toward looser monetary policy as a further growth spur. The signaling function of quantitative easing has
                                at times ensured that benchmark bond yields rose while the Fed was buying only to drop once the 
                                purchase program was discontinued. 
                                More information about QE can be 
                                found on [Quantitative easing](https://www.investopedia.com/terms/q/quantitative-easing.asp)
                                '''),
                        ])
                    ], color='dark', outline=True),
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

                                ##### Retail sales and its importance to the economy

                                The term retail sales refers to an economic metric that tracks consumer
                                demand for finished goods. This figure is a very important data set as 
                                it is a key monthly market-moving event. Retail sales are reported each month by the
                                U.S. Census Bureau and indicate **the direction of the economy**. It acts as a key economic barometer
                                and whether inflationary pressures exist. The historical retail sales data was collected 
                                from [FRED](https://fred.stlouisfed.org/)

                                More information about retail sales can be found on 
                                [Retail Sales](https://www.investopedia.com/terms/r/retail-sales.asp#:~:text=The%20term%20retail%20sales%20refers,the%20direction%20of%20the%20economy.)

                                '''),
                        ])
                    ], color='dark',  outline=True),
                ], width=12),], className = 'mb-2 mt-2'),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='s&p500-dxy', figure={}),
                        ])
                    ]),
                #],width=6),
                ], width=12),], className = 'mb-2 mt-2'),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Markdown('''

                                ##### Why is the US Dollar Index intersting

                                The US Dollar Index is important both as a market
                                in its own right and as it is an indicator of the relative strength 
                                of the US Dollar around the world. It can be used in technical 
                                analysis to confirm trends related to the following markets, among others:

                                * Commodities priced in USD
                                * Currency pairs that include the US Dollar (such as the ones used to calculate the index’s value)
                                * Stocks and indexes.
                                
                                The US Dollar Index data was collected from [US Dollar Index](https://www.investing.com/)

                                '''),
                        ])
                    ], color='dark', outline=True),
                ], width=12),], className = 'mb-2 mt-2'),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='s&p500-jobless', figure={}),

                        ])
                    ]),
                #],width=6),
                ], width=12),], className = 'mb-2 mt-2'),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Markdown('''

                                ##### Jobless claims and the economy    

                                A high unemployment rate affects the economy in many ways.
                                Unemployed people tend to spend less, may accrue more debt, and unemployment may
                                lead to higher payments from state and federal governments for things like food stamps.
                                The jobless claims data was collected from [FRED](https://fred.stlouisfed.org/)

                                More information about the unemployment impact on economy can be found on 
                                [The Cost of Unemployment to the Economy](https://www.investopedia.com/financial-edge/0811/the-cost-of-unemployment-to-the-economy.aspx)
                                '''),
                        ])
                    ], color='dark', outline=True),
                ], width=12),], className = 'mb-2 mt-2'),

                dbc.Row([
                    dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='s&p500-procentage', figure={}),

                            ])
                        ])
                    ],width=6),
                    
                    dbc.Col([
                    dcc.Dropdown(id='slc_oc',
                            options = [
                                {'label':'Open', 'value': 'Open'},
                                {'label':'Close', 'value':'Close'}
                            ],
                            multi = False,
                            value = 'Open',
                            style={'width':'100%'},
                    )
                    ], width=3), 

                    ]),
                    #], width=6),], className = 'mb-2 mt-2'),
                
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Markdown('''

                                    ##### What happens after a bloody day in the stock market

                                    This bar chart shows historicaly how the S&P500 have opened the next day after closing -3% or more on the daily
                                    frame.

                                    '''),
                            ])
                        ], style={"height": 480}, color='dark', outline=True),
                    ], width=6),], className = 'mb-2 mt-2')
        ]

@callback(
        Output('s&p500-i-rates', 'figure'),
        Output('s&p500-print', 'figure'),
        Output('s&p500-res', 'figure'),
        Output('s&p500-rsxfs', 'figure'),
        Output('s&p500-dxy', 'figure'),
        Output('s&p500-jobless', 'figure'),
        Output('s&p500-procentage', 'figure'),
        Input('slider-s&p500', 'value'),
        Input('slc_oc', 'value')
)

def update_data(correlation, op_cl):

        # def RockyBalboa():
            

        #S&P500 Historical data
        s_p500 = pd.read_csv('data/sp500_daily-1950-to-2022.csv')
        s_p500_filtered = s_p500.copy()
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

        #S&P500 data filtered
        s_p500_filtered = s_p500_filtered[s_p500_filtered.Date >= '1987-01-10'] #1976-01-10
        s_p500_filtered.Date = pd.to_datetime(s_p500_filtered.Date)
        s_p500_filtered = s_p500_filtered.set_index('Date')
        s_p500_filtered.index = s_p500_filtered.index.date

        #US Dollar Index
        df_DXY = pd.read_csv('data/DXY_historical_data_clean2.csv')
        df_DXY = df_DXY.drop(['Open', 'High', 'Low', 'Vol.', 'Change %'], axis=1)
        df_DXY = df_DXY.replace(',','', regex=True)
        df_DXY = df_DXY[df_DXY.Date >= '1987-01-10']
        df_DXY = df_DXY[df_DXY.Date <= '2022-04-01'] #2022-04-01
        df_DXY.Date = pd.to_datetime(df_DXY.Date)
        df_DXY = df_DXY.set_index('Date')
        df_DXY = df_DXY.apply(pd.to_numeric)
        df_DXY.index = df_DXY.index.date

        df4 = pd.read_csv('data/ICSA.csv')
        df4 = df4.rename(columns={'DATE':'Date'})
        df4 = df4[df4.Date >= '1987-01-10']
        df4 = df4[df4.Date <= '2022-04-01']
        df4.Date = pd.to_datetime(df4.Date)
        df4 = df4.set_index('Date')
        df4.index = df4.index.date

        #Porcentages data

        df_por = dp.porcentage_data(op_cl)
        por_values = dp.get_porc(df_por)

        #economic_df = dp.economic_calendar()

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


        fig5 = make_subplots(specs=[[{"secondary_y": True}]])
        fig5.add_trace(go.Scatter(x=s_p500_filtered.index, y=s_p500_filtered.Close,
                        mode='lines',
                        name='S&P500 price',
                        line=dict(color='rgb(64,64,64)',
                                    width=3)
                        ),secondary_y=True)
        
        fig5.add_trace(go.Scatter(x=df_DXY.index, y=df_DXY.Price,
                        mode='lines',
                        name='DXY',
                        line=dict(color='rgb(51,255,51)',
                                    width=3)
                        ),secondary_y=False)
        
        fig5.update_layout(
            title="<b>S&P500 & US Dollar Index</b>",
            font=dict(
                size=13,
                color="black"
            )
        )

        fig5.update_yaxes(title_text="<b>S&P500 price</b>", secondary_y=True, type='log')
        fig5.update_xaxes(title_text="<b>Date</b>")
        fig5.update_yaxes(title_text="<b>DXY</b>", secondary_y=False)

        fig6 = make_subplots(specs=[[{"secondary_y": True}]])
        fig6.add_trace(go.Scatter(x=s_p500_filtered.index, y=s_p500_filtered.Close,
                        mode='lines',
                        name='S&P500 price',
                        line=dict(color='rgb(64,64,64)',
                                    width=3)
                        ),secondary_y=True)
    
        fig6.add_trace(go.Scatter(x=df4.index, y=df4.ICSA,
                        mode='lines',
                        name='IC',
                        line=dict(color='rgb(222,58,58)',
                                    width=3)
                        ),secondary_y=False)
        
        fig6.update_layout(
            title="<b>S&P500 & Jobless Claims</b>",
            font=dict(
                size=13,
                color="black"
            )
        )

        fig6.update_yaxes(title_text="<b>S&P500 price</b>", secondary_y=True, type='log')
        fig6.update_xaxes(title_text="<b>Date</b>")
        fig6.update_yaxes(title_text="<b>IC</b>", secondary_y=False, type='log')

        fig7 = go.Figure([go.Bar(x=['Positive', 'Negative'], 
                                y=[por_values[0], por_values[1]]
                                )])
        
        fig7.update_traces(marker_color = ['rgb(31,242,87)', 'rgb(253,49,49)'], marker_line_color='rgb(0,0,0)',
                  marker_line_width=1.5, opacity=0.8)

#31,242,87
#253,49,49
        # fig7 = go.Figure(data=[go.Table(

        #         header=dict(values=list(economic_df.columns),
        #                     fill_color='#232345',
        #                     align='left'),

        #         cells=dict(values=[economic_df.id, economic_df.date, economic_df.time
        #         , economic_df.zone, economic_df.currency, economic_df.importance, economic_df.event,
        #         economic_df.actual, economic_df.forecast, economic_df.previous],
        #                 fill_color='lavender',
        #                 align='left'))
        #     ])

        # fig7 = dash_table.DataTable(
        #     # values = dict(values=[economic_df.id, economic_df.date, economic_df.time
        #     #       , economic_df.zone, economic_df.currency, economic_df.importance, economic_df.event,
        #     #       economic_df.actual, economic_df.forecast, economic_df.previous])
        #     data = economic_df.to_dict('records'),
        #     columns =[{'id': c, 'name':c} for c in economic_df.columns]

        #     )

        return fig1, fig2, fig3, fig4, fig5, fig6, fig7