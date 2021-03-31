import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import home, goals, consistency, tournaments, goals_predict

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Menu", className="display-4"),
        html.Hr(),

        dbc.Nav(
            [
                dbc.NavLink("Home", href="/Home", id="Home-Page"),
                dbc.NavLink("Goals", href="/Goals", id="Goals"),
                dbc.NavLink("Consistency", href="/Consistency", id="Consistency"),
                dbc.NavLink("Tournaments", href="/Tournaments", id="Tournaments"),
                dbc.NavLink("Goals Prediction", href="/Goals-Prediction", id="Goals-Prediction"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/Home":
        return home.layout
    elif pathname == "/Goals":
        return goals.layout
    elif pathname == "/Consistency":
        return consistency.layout
    elif pathname == "/Tournaments":
        return tournaments.layout
    elif pathname == "/Goals-Prediction":
        return goals_predict.layout


if __name__ == '__main__':
  app.run_server()
