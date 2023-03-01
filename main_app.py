import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import dcc
from dash.dependencies import Input, Output, State
from sidebar_pages import page0, page1, page5, page6, page7
from dash_extensions import Lottie

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# navbar = dbc.NavbarSimple(
#     children=[
#         dbc.Button("Sidebar", outline=True, color="secondary", className="mr-1", id="btn_sidebar")
#     ],

#     brand="Data Analysis",
#     brand_href="#",
#     color="dark",
#     dark=True,
#     fluid=True,
# )
url = 'https://assets8.lottiefiles.com/packages/lf20_lljs8qwh.json'
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

navbar = dbc.Navbar(
    dbc.Container([
        html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        #dbc.Col(Lottie(options=options, width="15%", height="15%", url=url)),
                        dbc.Col(html.H2(children='Data Analysis',
                                    style={
                                        'textAlign':'center',
                                        'color': '#FFFFFF'
                                    }, className='ms-2')),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
        # html.Img(src=PLOTLY_LOGO, height="30px"),
        # html.Img(src=PLOTLY_LOGO, height="30px"),
        # html.H2(children='Economic calendar',
        #         style={
        #             'textAlign':'center',
        #             'color': '#FFFFFF'
        #         }),
        #dbc.Button("Sidebar", outline=True, color="secondary", className="mr-1", id="btn_sidebar")
        html.Button(id='btn_sidebar', children=[html.Img(src='assets/sidebar_img.png')]),
    ]),
    color='dark',
    dark=True,
    style={
        "position": "sticky",
        "top":0,
        "z-index": 9999}
)

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "4rem",
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "90%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    #"padding": "0.5rem 1rem",
    "padding": "4rem 1rem 2rem",
    #"background-color": "#47627d",
    "background-color": "#3399FF",
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
    #"padding": "0rem 0rem",
    "padding": "4rem 1rem 2rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "top": 0,
    "left": 0,
    "bottom": 0,
    #"padding-top": "55px",
    "overflow-x": "hidden",
    "overflow":"scroll",
    "height":"70%",
    "z-index": 1
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "top": "12rem",
    #"padding-top": "55px",
    #"overflow":"fixed"
    # "overflow":"auto",
    "height":"90%",
    #"z-index": 1
}

NAVBAR_STYLE = {
    "color": "#fff",
    "font-size": "16px",
    # "position": "sticky",
    # "top":0,
    # "z-index": 100
    #"left": '16px',
    #"font-weight": 700,
    #"background-color": "#bedbf7",
}

sidebar = html.Div(
    [
        html.H3(children='Beta 1.0 Metrics',
            style={
                'textAlign':'center',
                'color': '#FFFFFF'
            }),
        html.Hr(),
        html.P(
            "Metrics for analysis", className="lead"
        ),

        dbc.Nav(
            [
                dbc.NavLink("Main page", href="/", active="exact", style=NAVBAR_STYLE),
                dbc.NavLink("Crypto metrics", href="/page-1", active="exact", style=NAVBAR_STYLE),
                # dbc.NavLink("Crypto adresses growth", href="/page-2", active="exact", style=NAVBAR_STYLE),
                # dbc.NavLink("Crypto twitter growth", href="/page-3", active="exact", style=NAVBAR_STYLE),
                # dbc.NavLink("Crypto total sentiment", href="/page-4", active="exact", style=NAVBAR_STYLE),
                dbc.NavLink('Bitcoin analysis metrics', href="/page-5", active="exact", style=NAVBAR_STYLE),
                dbc.NavLink('S&P 500 metrics', href="/page-6", active="exact", style=NAVBAR_STYLE),
                dbc.NavLink('Currencies', href="/page-7", active="exact", style=NAVBAR_STYLE),
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

    elif pathname == "/page-5":
        return page5.layout

    elif pathname == "/page-6":
        return page6.layout
    
    elif pathname == "/page-7":
        return page7.layout
        
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
