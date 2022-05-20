import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import dcc
from dash.dependencies import Input, Output, State
from sidebar_pages import page0, page1, page2, page3, page4, page5, page6

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

navbar = dbc.NavbarSimple(
    children=[
        dbc.Button("Sidebar", outline=True, color="secondary", className="mr-1", id="btn_sidebar")
    ],
    brand="Data Analysis",
    brand_href="#",
    color="dark",
    dark=True,
    fluid=True,
)

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    #"background-color": "#47627d",
    "background-color": "#333741",
    "overflow":"scroll",
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 0,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
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
    id="sidebar",
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Store(id='side_click'),
    dcc.Location(id="url"),
    navbar,
    sidebar,
    content
])

@app.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):

    if pathname == "/":
        return page0.layout

    elif pathname == "/page-1":
        return page1.layout

    elif pathname == "/page-2":
        return page2.layout

    elif pathname == "/page-3":
        return page3.layout

    elif pathname == "/page-4":
        return page4.layout
        
    elif pathname == "/page-5":
        return page5.layout

    elif pathname == "/page-6":
        return page6.layout
        
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

#DONE implement bootstrap for all of the pages and implement new metrics
#DONE implement logarithmic scale options
#TODO implement new metrics section for total crypto asset class
#DONE solve loading time problems

if __name__=='__main__':
    app.run_server(debug=True)#, port=3000)
