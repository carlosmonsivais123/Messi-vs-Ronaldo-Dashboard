import dash
import dash_bootstrap_components as dbc

# meta_tags are required for the app layout to be mobile responsive
FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP, FA])
server = app.server
