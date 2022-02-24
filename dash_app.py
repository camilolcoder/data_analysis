# Code source: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go

import data_processing as dp
import datetime as dt
import pandas as pd

from plotly.subplots import make_subplots

# data source: https://www.kaggle.com/chubak/iranian-students-from-1968-to-2017
# data owner: Chubak Bidpaa
df = pd.read_csv('https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Bootstrap/Side-Bar/iranian_students.csv')

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
                dbc.NavLink("Crypto vs trending", href="/", active="exact", style=NAVBAR_STYLE),
                dbc.NavLink("Crypto sentiment", href="/page-1", active="exact", style=NAVBAR_STYLE),
                dbc.NavLink("Crypto on-chain data", href="/page-2", active="exact", style=NAVBAR_STYLE),
                dbc.NavLink("Crypto social presence", href="/page-3", active="exact", style=NAVBAR_STYLE),
                dbc.NavLink("working...", href="/page-4", active="exact", style=NAVBAR_STYLE),
                dbc.NavLink('Bold', href="/page-5", active="exact", style=NAVBAR_STYLE),
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
    figo = go.Figure(go.Bar(x=['positive', 'negative'],y=[43 , 67]))

    figo.update_traces(marker_color=['rgb(250,38,52)', 'rgb(65,255,78)'], marker_line_color='rgb(0,0,0)',
                  marker_line_width=2, opacity=0.6)
    #figo = px.bar([['positive', 'negative'],[positive , negative]], x='sentiment', y='pop')
    #title="Plot Title",

    figo.update_layout(
    xaxis_title="<b>Bitcoin sentiment</b>",
    yaxis_title="<b>Sentiment points</b>",
    legend_title="Legend Title",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="Black" 
    ))

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
                html.H1('Crypto sentiment',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=figo)
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
                # html.H1('High School in Iran',
                #         style={'textAlign':'center'}),
                # dcc.Graph(id='bargraph',
                #          figure=px.bar(df, barmode='group', x='Years',
                #          y=['Girls High School', 'Boys High School']))

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
                html.H1('Graph testing',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=px.bar(df, barmode='group', x='Years',
                         y=['Girls High School', 'Boys High School']))
                ]
    elif pathname == "/page-5":
        return [
                dbc.Row([
                    dbc.Col([
                        html.H2("Financial Analysis", style={'text_align':'center'}),
                    ],width=2),
                    dbc.Col([
                        dcc.Dropdown(id='slct_year',
                                options=[
                                    {'label':'2021','value': 2021},
                                    {'label':'2022','value': 2022}
                                    ],
                                multi = False,
                                value = 2022,
                                style={'width':'100%'},
                                ),        
                    html.Div(id='output_container_years', children=[]),
                    html.Br()
                    ],width=2)]),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='pie-chart', figure={}),
                            ])
                        ]),
                    ], width=6),])

        ]      
        

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

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

    fig.update_yaxes(title_text="<b>Crypto price</b>", secondary_y=True)
    fig.update_yaxes(title_text="<b>Trending values</b>", secondary_y=False)

    fig.update_layout(
    font_color="black",
    )

    return fig #, figo

@app.callback(
        #Output('crypto-trending', 'figure'),
        Output('pie-chart', 'figure'),
        #Input('crypto_name', 'value'),
        Input('slct_year', 'value')
)

def update_data(year):

    if year == 2021:
        figo = go.Figure(go.Bar(x=['positive', 'negative'],y=[43 , 67]))
    elif year == 2022:
        figo = go.Figure(go.Bar(x=['positive', 'negative'],y=[67 , 43]))

    return figo

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


#TODO implement bootstrap for all of the pages and implement new metrics

if __name__=='__main__':
    app.run_server(debug=True, port=3000)
