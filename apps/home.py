import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly_dark"
import pandas as pd
import datetime
import pathlib
import base64
from app import app

########################################### Data ###################################################
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

messi = pd.read_excel(DATA_PATH.joinpath("messi clean.xlsx"))
ronaldo = pd.read_excel(DATA_PATH.joinpath("ronaldo clean.xlsx"))

########################################### Table
clutch_messi = messi[['Dates', 'Result', 'Win Draw Loss', 'Competition',
                             'General Competition', 'Round', 'Venue', 'Squad', 'Opponent',
                             'Game Started', 'Minutes', 'Played', 'Goals', "Assists"]].copy()
clutch_messi["Player"] = "Lionel Messi"

clutch_ronaldo = ronaldo[['Dates', 'Result', 'Win Draw Loss', 'Competition',
                                 'General Competition', 'Round', 'Venue', 'Squad', 'Opponent',
                                 'Game Started', 'Minutes', 'Played', 'Goals', "Assists"]].copy()
clutch_ronaldo["Player"] = "Cristiano Ronaldo"


both_players = pd.concat([clutch_messi, clutch_ronaldo])
both_players.reset_index(inplace = True, drop = True)

ronaldo_table = []
messi_table = []

value_names = ["Win Percentage", "Draw Percentage", "Loss Percentage", "Wins", "Draws", "Losses", "Games Played",
               "Goals", "Assists", "Goals per Game", "Assists per Game", "Contributions per Game (Goals + Assists)"]

###### Win % #######
wdl_table = both_players[["Win Draw Loss", "Player", "Goals"]].groupby(["Player", "Win Draw Loss"]).count().T
played = both_players[["Dates", "Player"]].groupby(["Player"]).count().T

ronaldo_table.append("{}%".format(round(wdl_table["Cristiano Ronaldo"]["W"].tolist()[0] / played["Cristiano Ronaldo"].tolist()[0] * 100, 2)))
messi_table.append("{}%".format(round(wdl_table["Lionel Messi"]["W"].tolist()[0] / played["Lionel Messi"].tolist()[0] * 100, 2)))

###### Draw % #######
ronaldo_table.append("{}%".format(round(wdl_table["Cristiano Ronaldo"]["D"].tolist()[0] / played["Cristiano Ronaldo"].tolist()[0] * 100, 2)))
messi_table.append("{}%".format(round(wdl_table["Lionel Messi"]["D"].tolist()[0] / played["Lionel Messi"].tolist()[0] * 100, 2)))

###### Loss % #######
ronaldo_table.append("{}%".format(round(wdl_table["Cristiano Ronaldo"]["L"].tolist()[0] / played["Cristiano Ronaldo"].tolist()[0] * 100, 2)))
messi_table.append("{}%".format(round(wdl_table["Lionel Messi"]["L"].tolist()[0] / played["Lionel Messi"].tolist()[0] * 100, 2)))

###### WDL #######
ronaldo_table.append(wdl_table["Cristiano Ronaldo"]["W"].tolist()[0])
ronaldo_table.append(wdl_table["Cristiano Ronaldo"]["D"].tolist()[0])
ronaldo_table.append(wdl_table["Cristiano Ronaldo"]["L"].tolist()[0])
messi_table.append(wdl_table["Lionel Messi"]["W"].tolist()[0])
messi_table.append(wdl_table["Lionel Messi"]["D"].tolist()[0])
messi_table.append(wdl_table["Lionel Messi"]["L"].tolist()[0])

###### Played #######
ronaldo_table.append(played["Cristiano Ronaldo"].tolist()[0])
messi_table.append(played["Lionel Messi"].tolist()[0])

###### Goals #######
goals = both_players[["Goals", "Player"]].groupby(["Player"]).sum().T
ronaldo_table.append(goals["Cristiano Ronaldo"].tolist()[0])
messi_table.append(goals["Lionel Messi"].tolist()[0])

###### Assists #######
assists = both_players[["Assists", "Player"]].groupby(["Player"]).sum().T
ronaldo_table.append(assists["Cristiano Ronaldo"].tolist()[0])
messi_table.append(assists["Lionel Messi"].tolist()[0])

###### Goals per Game #######
ronaldo_table.append(round((goals["Cristiano Ronaldo"].tolist()[0]) / played["Cristiano Ronaldo"].tolist()[0], 2))
messi_table.append(round((goals["Lionel Messi"].tolist()[0]) / played["Lionel Messi"].tolist()[0], 2))

###### Assists per Game #######
ronaldo_table.append(round((assists["Cristiano Ronaldo"].tolist()[0]) / played["Cristiano Ronaldo"].tolist()[0], 2))
messi_table.append(round((assists["Lionel Messi"].tolist()[0]) / played["Lionel Messi"].tolist()[0], 2))

###### Contribution Per Game #######
ronaldo_table.append(round((goals["Cristiano Ronaldo"].tolist()[0] + assists["Cristiano Ronaldo"].tolist()[0]) / played["Cristiano Ronaldo"].tolist()[0], 2))
messi_table.append(round((goals["Lionel Messi"].tolist()[0] + assists["Lionel Messi"].tolist()[0]) / played["Lionel Messi"].tolist()[0], 2))

# Reading in Image
image_filename = 'assets/mvr.jpg' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

########################################### Application ###################################################
layout = html.Div([
                  html.Div(html.H1(["Lionel Messi VS Cristiano Ronaldo",html.Br(),html.H3("Dashboard Created By: Carlos Monsivais")]), style = {'backgroundColor' : '#181818', 'display': 'inline-block', 'verticalAlign': 'top',
                                                                                    "width": "100%", "color": "gold"}),

                   html.Div([html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))], style={'padding' : '0px', 'textAlign': 'center', 'backgroundColor' : '#686868'}),

                  html.Div(html.H4('''Welcome to my Messi vs Ronaldo Dashboard!'''), style = {'backgroundColor' : '#181818', 'display': 'inline-block', 'verticalAlign': 'top',
                                                                                    "width": "100%", "color": "gold"}),

                  html.Div('''Lionel Messi and Cristiano Ronaldo are both amazing players and considered to be the best of all time.
                  Through the use of this dashboard we are able to statistically compare which player is better in terms of goal scoring
                  abilities, best in crucial situations and consistency. Both players have very different play styles however at the end of
                  the day, hopefully this dashboard will help you make a more informed decision as to which player you think
                  is better.''', style = {'backgroundColor' : '#181818', 'display': 'inline-block', 'verticalAlign': 'top',
                                                                                  "width": "100%", "color": "white", 'fontSize': 16}),


                   html.Div(dcc.Graph(id = "summary_table",
                                      figure = {"data": [go.Table(
                                                  header=dict(values=list(["", "Lionel Messi", "Cristiano Ronaldo"]),
                                                              fill_color='#222831',
                                                              line_color='white',
                                                              font=dict(color='white', size=13),
                                                              align='center'),
                                                  cells=dict(values=[value_names, messi_table, ronaldo_table], font=dict(color='white', size=13)))],
                                                "layout": go.Layout(title={'text': "Player Summaries", 'x':0.5},
                                                                    template= "plotly_dark",
                                                                    paper_bgcolor = '#222831')}),
                                      style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '100%'})

                            ], style = {'text-align': 'center'})
