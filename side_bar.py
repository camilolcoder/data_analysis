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


# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Main metrics", className="display-4"),
        html.Hr(),
        html.P(
            "Metrics for analysis", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Crypto vs trending", href="/", active="exact"),
                dbc.NavLink("Crypto sentiment", href="/page-1", active="exact"),
                dbc.NavLink("Crypto on-chain data", href="/page-2", active="exact"),
                dbc.NavLink("Crypto project activity", href="/page-3", active="exact"),
                dbc.NavLink("working...", href="/page-4", active="exact"),
                dbc.NavLink("working...", href="/page-5", active="exact"),
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
    fig = make_subplots(specs=[[{"secondary_y": True}]])#go.Figure()
    df1 = dp.collect_trend_score('crypto', 1)
    columns = df1.columns
    #df2 = dp.get_binance_bars('BTCUSDT', '1d', dt.datetime(2020, 1, 1), dt.datetime(2022, 2, 1))
    df2 = dp.crypto_data()

    fig.add_trace(go.Scatter(x=df1.index, y=df1[columns[0]],
                    mode='lines',
                    name='trending',
                    line=dict(color='rgb(153,204,255)',
                                width=2)
                    ),secondary_y=True)

    fig.add_trace(go.Scatter(x=df2.index, y=df2.closePriceUsd,
                    mode='lines',
                    name='BTC price',
                    line=dict(color='rgb(128,255,0)',
                                width=2)
                    ),secondary_y=False)
    
    # fig.update_traces(marker_color=['rgb(250,38,52)', 'rgb(65,255,78)'],
    #               marker_line_width=2)

    fig.update_yaxes(title_text="<b>BTC price</b>", secondary_y=True)
    fig.update_yaxes(title_text="<b>Trending values</b>", secondary_y=False)
    #positive, negative = dp.search_sentiment('Bitcoin')

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

    growth_df = dp.crypto_growth()

    fig_growth = go.Figure()

    fig_growth.add_trace(go.Scatter(x = growth_df.index, y = growth_df.value,
                                    mode = 'lines',
                                    name = 'new adresses',
                                    line=dict(color='rgb(128,255,0)',
                                    width=2)))


    if pathname == "/":
        return [
                html.H1('Crypto trending',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=fig)
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
                html.H1('Crypto growth',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=fig_growth)
                ]
    elif pathname == "/page-3":
        return [
                html.H1('High School in Iran',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=px.bar(df, barmode='group', x='Years',
                         y=['Girls High School', 'Boys High School']))
                ]
    elif pathname == "/page-4":
        return [
                html.H1('High School in Iran',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=px.bar(df, barmode='group', x='Years',
                         y=['Girls High School', 'Boys High School']))
                ]
    elif pathname == "/page-5":
        return [
                html.H1('High School in Iran',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=px.bar(df, barmode='group', x='Years',
                         y=['Girls High School', 'Boys High School']))
                ]
    # elif pathname == "/page-2":
    #     return [
    #             html.H1('High School in Iran',
    #                     style={'textAlign':'center'}),
    #             dcc.Graph(id='bargraph',
    #                      figure=px.bar(df, barmode='group', x='Years',
    #                      y=['Girls High School', 'Boys High School']))
    #             ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__=='__main__':
    app.run_server(debug=True, port=3000)
