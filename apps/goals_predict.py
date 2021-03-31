import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from datetime import date
import warnings
warnings.filterwarnings('ignore')
import datetime
import pathlib
import plotly.express as px
from app import app
import plotly.io as pio
import dash_table
from statsmodels.tsa.seasonal import seasonal_decompose
pio.templates.default = "plotly_dark"

from statsmodels.tsa.statespace.sarimax import SARIMAXResults
import math

########################################### Data ###################################################
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
MODEL_PATH = PATH.joinpath("../assets").resolve()

messi = pd.read_excel(DATA_PATH.joinpath("messi clean.xlsx"))
ronaldo = pd.read_excel(DATA_PATH.joinpath("ronaldo clean.xlsx"))

messi_mode_loaded = SARIMAXResults.load(MODEL_PATH.joinpath("messi_ts_model.pkl"))
ronaldo_mode_loaded = SARIMAXResults.load(MODEL_PATH.joinpath("ronaldo_ts_model.pkl"))

# Only getting matches that he played in.
messi.dropna(axis =1, inplace = True)
messi = messi[messi["Played"] ==  "Played"].copy()
messi.reset_index(inplace = True, drop = True)

messi_gpm = messi.copy()
messi_gpm.set_index(keys = "Dates", inplace = True, drop = True)
messi_gpm = messi_gpm.resample("W").sum()
messi_gpm["Dates 2"] = messi_gpm.index
messi_gpm["Dates 2"] = pd.to_datetime(messi_gpm["Dates 2"]).dt.date

age = []
for value in messi_gpm["Dates 2"]:
    from dateutil.relativedelta import relativedelta
    import datetime
    difference_in_years = relativedelta(value, datetime.date(1987, 6, 24)).years
    age.append(difference_in_years)

messi_gpm["Age"] = age
messi_gpm["Cummulative Goals Weekly"] = messi_gpm["Goals"].cumsum()
messi_gpm = messi_gpm[["Cummulative Goals Weekly", "Age"]].copy()

# Only getting matches that he played in.
ronaldo.dropna(axis =1, inplace = True)
ronaldo = ronaldo[ronaldo["Played"] ==  "Played"].copy()
ronaldo.reset_index(inplace = True, drop = True)

ronaldo_gpm = ronaldo.copy()
ronaldo_gpm.set_index(keys = "Dates", inplace = True, drop = True)
ronaldo_gpm = ronaldo_gpm.resample("W").sum()
ronaldo_gpm["Dates 2"] = ronaldo_gpm.index
ronaldo_gpm["Dates 2"] = pd.to_datetime(ronaldo_gpm["Dates 2"]).dt.date

age = []
for value in ronaldo_gpm["Dates 2"]:
    from dateutil.relativedelta import relativedelta
    import datetime
    difference_in_years = relativedelta(value, datetime.date(1985, 2, 5)).years
    age.append(difference_in_years)

ronaldo_gpm["Age"] = age
ronaldo_gpm["Cummulative Goals Weekly"] = ronaldo_gpm["Goals"].cumsum()
ronaldo_gpm = ronaldo_gpm[["Cummulative Goals Weekly", "Age"]].copy()

# Decompositions
messi_decompose = seasonal_decompose(messi_gpm["Cummulative Goals Weekly"], model='additive', two_sided = False)
messi_dec_trend = pd.DataFrame(messi_decompose.trend)
messi_dec_seas = pd.DataFrame(messi_decompose.seasonal)
messi_dec_res = pd.DataFrame(messi_decompose.resid)

ronaldo_decompose = seasonal_decompose(ronaldo_gpm["Cummulative Goals Weekly"], model='additive', two_sided = False)
ronaldo_dec_trend = pd.DataFrame(ronaldo_decompose.trend)
ronaldo_dec_seas = pd.DataFrame(ronaldo_decompose.seasonal)
ronaldo_dec_res = pd.DataFrame(ronaldo_decompose.resid)


def train_test_data(df, split):
    indexed = math.floor(len(df) * split)
    training = df.iloc[0:indexed,:]
    testing = df.iloc[indexed:,:]

    return training, testing

messi_train_test_split = train_test_data(messi_gpm, 0.8)

training_messi_data = messi_train_test_split[0]
testing_messi_data = messi_train_test_split[1]


ronaldo_train_test_split = train_test_data(ronaldo_gpm, 0.8)

training_ronaldo_data = ronaldo_train_test_split[0]
testing_ronaldo_data = ronaldo_train_test_split[1]


########################################### Dropdown Options ###################################################

########################################## Application ###################################################
layout = html.Div([
                    html.Div(html.H1("Career Goals Prediction: Time Series Analysis"), style = {'padding' : '0px',
                                                                'backgroundColor' : '#181818', 'display': 'inline-block', 'verticalAlign': 'top',
                                                                "width": "100%", "color": "gold"}),

                    html.Div('''In order to predict the cumulative goals scored per player, which can also be seen as the career amount of goals a player
                    has scored I am going to use a SARIMA Time Series model for Lionel Messi and Cristiano Ronaldo.''',
                    style = {'backgroundColor' : '#181818', 'display': 'inline-block', 'verticalAlign': 'top',
                             "width": "100%", "color": "white", 'fontSize': 18}),

                    html.Div(html.H3("Cumulative Goals per Week"), style = {'padding' : '0px',
                                                             'backgroundColor' : '#686868', 'display': 'inline-block', 'verticalAlign': 'top',
                                                              "width": "100%", "color": "gold"
                                                             }),

                    html.Div('''Below are Lionel Messi and Cristiano Ronaldo's goals over time throughout their careers. These are the values that we
                    are going to train and forecast over the players careers.''',
                    style = {'backgroundColor' : '#686868', 'display': 'inline-block', 'verticalAlign': 'top',
                             "width": "100%", "color": "white", 'fontSize': 14}),

                    html.Div(dcc.Graph(id = "goal graphs",
                                       figure = {"data": [go.Scatter(x = messi_gpm.index, y = messi_gpm["Cummulative Goals Weekly"], name = "Messi"),
                                                        go.Scatter(x = ronaldo_gpm.index, y = ronaldo_gpm["Cummulative Goals Weekly"], name="Ronaldo")],
                                               "layout": go.Layout(title={'text': "Cumulative Goals Scored Weekly", 'x':0.5},
                                                                   legend=dict(orientation="h", x=0.40, y=1.15),
                                                                   template = "plotly_dark",
                                                                   paper_bgcolor = '#686868')}),
                                       style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '100%'}),

                    html.Div(html.H3("Time Series Decomposition per Player"), style = {'padding' : '0px',
                                                             'backgroundColor' : '#222831', 'display': 'inline-block', 'verticalAlign': 'top',
                                                              "width": "100%", "color": "gold"
                                                             }),

                    html.Div('''Here we can compare the decomposition of both of the players career goals over time. As we can see, the trend,
                    seasonality and residuals of each player show us that there is a quickly rising upward trend and seasonality to their goals scored.''',
                    style = {'backgroundColor' : '#222831', 'display': 'inline-block', 'verticalAlign': 'top',
                             "width": "100%", "color": "white", 'fontSize': 14}),

                    html.Div(dcc.Graph(id = "trend",
                                       figure = {"data": [go.Scatter(x = messi_dec_trend.index, y = messi_dec_trend.trend, name = "Messi"),
                                                        go.Scatter(x = ronaldo_dec_trend.index, y = ronaldo_dec_trend.trend, name = "Ronaldo")],
                                               "layout": go.Layout(title={'text': "Trend Decomposition", 'x':0.5},
                                                                   legend=dict(orientation="h", x=0.2, y=1.15),
                                                                   template = "plotly_dark",
                                                                   paper_bgcolor = '#222831')}),
                                       style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '33.33%'}),

                    html.Div(dcc.Graph(id = "seasonality",
                                       figure = {"data": [go.Scatter(x = messi_dec_seas.index, y = messi_dec_seas.seasonal, name = "Messi"),
                                                        go.Scatter(x = ronaldo_dec_seas.index, y = ronaldo_dec_seas.seasonal, name = "Ronaldo")],
                                               "layout": go.Layout(title={'text': "Seasonal Decomposition", 'x':0.5},
                                                                   legend=dict(orientation="h", x=0.2, y=1.15),
                                                                   template = "plotly_dark",
                                                                   paper_bgcolor = '#222831')}),
                                       style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '33.33%'}),

                    html.Div(dcc.Graph(id = "residuals",
                                       figure = {"data": [go.Scatter(x = messi_dec_res.index, y = messi_dec_res.resid, name = "Messi"),
                                                        go.Scatter(x = ronaldo_dec_res.index, y = ronaldo_dec_res.resid, name = "Ronaldo")],
                                               "layout": go.Layout(title={'text': "Residual Decomposition", 'x':0.5},
                                                                   legend=dict(orientation="h", x=0.2, y=1.15),
                                                                   template = "plotly_dark",
                                                                   paper_bgcolor = '#222831')}),
                                       style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '33.33%'}),


                    html.Div(html.H3("Cummulative Goals per Week Predictions"), style = {'padding' : '0px',
                                                             'backgroundColor' : '#686868', 'display': 'inline-block', 'verticalAlign': 'top',
                                                              "width": "100%", "color": "gold"
                                                             }),

                    html.Div('''Below you can pick a date range between 12/10/2017 and 12/15/2024 because it assumes Lionel Messi and Cristiano Ronaldo
                    will play at a top level until then. To see how many goals a player will score be forecasted at a different date change the calendar
                    filters below.''',
                    style = {'backgroundColor' : '#686868', 'display': 'inline-block', 'verticalAlign': 'top',
                             "width": "100%", "color": "white", 'fontSize': 14}),

                    html.Div(dcc.DatePickerRange(
                        id = 'my-date-picker-range',
                        start_date_placeholder_text="Start Period",
                        end_date_placeholder_text="End Period",
                        calendar_orientation='vertical',
                        start_date=date(2017, 12, 10),
                        end_date=date(2021, 3, 28),
                        min_date_allowed=date(2017, 12, 10),
                        max_date_allowed=date(2025, 12, 15),
                    ), style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '100%', 'backgroundColor' : '#686868'}),

                    html.Div(html.H6(id='output-container-date-picker-range'), style = {'padding' : '0px',
                                                             'backgroundColor' : '#686868', 'display': 'inline-block', 'verticalAlign': 'top',
                                                              "width": "100%", "color": "white"
                                                             }),

                    html.Div(dcc.Graph(id = "predictions_graph_messi"),
                                      style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),

                    html.Div(dcc.Graph(id = "predictions_graph_ronaldo"),
                                      style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),


                    html.Div(id = "text_messi",
                            style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%', 'backgroundColor' : '#686868',
                            "color": "white", 'fontSize': 18}),

                    html.Div(id = "text_ronaldo",
                            style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%', 'backgroundColor' : '#686868',
                            "color": "white", 'fontSize': 18}),


                    html.Div(dcc.Graph(id = "predictions_table_messi"),
                                      style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),

                    html.Div(dcc.Graph(id = "predictions_table_ronaldo"),
                                      style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'})

], style = {'text-align': 'center'})

########################################### Callbacks ###################################################
@app.callback(Output('output-container-date-picker-range', 'children'),
             [Input('my-date-picker-range', 'start_date'),
              Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = ''
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Prediction Start Date: ' + start_date_string + ' and '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Prediction End Date: ' + end_date_string
    if len(string_prefix) == len(''):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix

@app.callback([Output('predictions_graph_messi', 'figure'),
               Output('predictions_table_messi', 'figure'),
               Output('predictions_graph_ronaldo', 'figure'),
               Output('predictions_table_ronaldo', 'figure'),
               Output('text_messi', 'children'),
               Output('text_ronaldo', 'children')],
             [Input('my-date-picker-range', 'start_date'),
              Input('my-date-picker-range', 'end_date')])
def update_output2(start_date, end_date):
    start_date_object = date.fromisoformat(start_date)
    input1_messi = pd.Timestamp(start_date_object, freq='W-SUN')

    end_date_object = date.fromisoformat(end_date)
    input2_messi = pd.Timestamp(end_date_object, freq='W-SUN')

    messi_predictions2 = pd.DataFrame(messi_mode_loaded.predict(start = input1_messi, end = input2_messi))
    messi_predictions2["Actuals"] = testing_messi_data["Cummulative Goals Weekly"]

    ronaldo_predictions2 = pd.DataFrame(ronaldo_mode_loaded.predict(start = input1_messi, end = input2_messi))
    ronaldo_predictions2["Actuals"] = testing_ronaldo_data["Cummulative Goals Weekly"]

    traces = []
    traces.append(go.Scatter(x = messi_predictions2.index, y = round(messi_predictions2.predicted_mean, 0), name = "Predictions"))
    traces.append(go.Scatter(x = messi_gpm.index, y = messi_gpm["Cummulative Goals Weekly"], name = "Testing Data"))
    traces.append(go.Scatter(x = training_messi_data.index, y = training_messi_data["Cummulative Goals Weekly"], name = "Training Data"))

    dates = list(messi_predictions2.index.date)
    predicts = list(round(messi_predictions2["predicted_mean"], 0))
    actuals = list(messi_predictions2["Actuals"])

    traces2 = []
    traces2.append(go.Table(
                            header=dict(values=list(["Date", "Predicted Goals", "Actual Goals"]),
                            fill_color='#222831',
                            line_color='white',
                            font=dict(color='white', size=13),
                            align='center'),
                cells=dict(values=[dates, predicts, actuals]
                )))

    traces3 = []
    traces3.append(go.Scatter(x = ronaldo_predictions2.index, y = round(ronaldo_predictions2.predicted_mean, 0), name = "Predictions"))
    traces3.append(go.Scatter(x = ronaldo_gpm.index, y = ronaldo_gpm["Cummulative Goals Weekly"], name = "Testing Data"))
    traces3.append(go.Scatter(x = training_ronaldo_data.index, y = training_ronaldo_data["Cummulative Goals Weekly"], name = "Training Data"))

    dates2 = list(ronaldo_predictions2.index.date)
    predicts2 = list(round(ronaldo_predictions2["predicted_mean"], 0))
    actuals2 = list(ronaldo_predictions2["Actuals"])

    traces4 = []
    traces4.append(go.Table(
                            header=dict(values=list(["Date", "Predicted Goals", "Actual Goals"]),
                            fill_color='#222831',
                            line_color='white',
                            font=dict(color='white', size=13),
                            align='center'),
                cells=dict(values=[dates2, predicts2, actuals2]
                )))

    messi_str_goals = "Lionel Messi Predicted Career Goals: {}".format(predicts[-1])
    ronaldo_str_goals = "Cristiano Ronaldo Predicted Career Goals: {}".format(predicts2[-1])

    return [{"data": traces, "layout": go.Layout(title={'text': "Messi Time Series Model", 'x':0.5},
                                                legend=dict(orientation="h", x=0.10, y=1.15),
                                                template = "plotly_dark",
                                                paper_bgcolor = '#686868')},

            {"data": traces2, "layout": go.Layout(title={'text': "Predictions Table Messi", 'x':0.5},
                              height = 450,
                              template= "plotly_dark",
                              paper_bgcolor = '#686868')},

            {"data": traces3, "layout": go.Layout(title={'text': "Ronaldo Time Series Model", 'x':0.5},
                            legend=dict(orientation="h", x=0.10, y=1.15),
                            template = "plotly_dark",
                            paper_bgcolor = '#686868')},

            {"data": traces4, "layout": go.Layout(title={'text': "Predictions Table Ronaldo", 'x':0.5},
                              height = 450,
                              template= "plotly_dark",
                              paper_bgcolor = '#686868')},

            messi_str_goals,

            ronaldo_str_goals
                              ]
