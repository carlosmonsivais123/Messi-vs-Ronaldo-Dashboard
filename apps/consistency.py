import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import datetime
import pathlib
from app import app

########################################### Data ###################################################
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

messi = pd.read_excel(DATA_PATH.joinpath("messi clean.xlsx"))
ronaldo = pd.read_excel(DATA_PATH.joinpath("ronaldo clean.xlsx"))

messi_minutes_per_year = pd.DataFrame(messi['Minutes'].groupby(messi.Dates.dt.to_period("Y")).agg('mean'))
messi_minutes_per_year.reset_index(inplace = True, drop = False)
messi_minutes_per_year["Dates"] = messi_minutes_per_year["Dates"].astype(str)
messi_minutes_per_year["Dates"] = pd.to_datetime(messi_minutes_per_year["Dates"])
messi_minutes_per_year["Minutes"] = round(messi_minutes_per_year["Minutes"], 0).astype('int')

ronaldo_minutes_per_year = pd.DataFrame(ronaldo['Minutes'].groupby(ronaldo.Dates.dt.to_period("Y")).agg('mean'))
ronaldo_minutes_per_year.reset_index(inplace = True, drop = False)
ronaldo_minutes_per_year["Dates"] = ronaldo_minutes_per_year["Dates"].astype(str)
ronaldo_minutes_per_year["Dates"] = pd.to_datetime(ronaldo_minutes_per_year["Dates"])
ronaldo_minutes_per_year["Minutes"] = round(ronaldo_minutes_per_year["Minutes"], 0).astype('int')

messi_average_cummulative_games_with_no_goals = round(messi["Games With no Goal"].mean(), 2)
ronaldo_average_cummulative_games_with_no_goals = round(ronaldo["Games With no Goal"].mean(), 2)

messi_played = [messi["Played"].value_counts()[0], messi["Played"].value_counts()[1]]
ronaldo_played = [ronaldo["Played"].value_counts()[0], ronaldo["Played"].value_counts()[1]]
########################################### Application ###################################################
layout = html.Div([html.Div(html.H1("Consistency"), style = {'padding' : '0px',
                                                                'backgroundColor' : '#181818', 'display': 'inline-block', 'verticalAlign': 'top',
                                                                "width": "100%", "color": "gold"}),

                    html.Div(html.H3("Consecutive Matches Played Without a Goal Scored"), style = {'text-align': 'center', 'font-weight': 'bold', 'display': 'inline-block',
                                                                        'verticalAlign': 'top', 'width': '100%', 'backgroundColor' : '#222831', "color": 'gold'}),

                    html.Div('''As a way to measure consistency in terms of goal scoring abilities, you can see the average matches each player
                    goes without scoring a goal. With this in mind, below are some heat maps showing all the games each player has played in
                    while the metric of the matches without a goal is displayed along with the match outcome. From the heat maps, the biggest
                    takeaway is that both players don't go much time without scoring, with the only exception being early in their careers
                    which is expected when starting out. Towards the bottom of this section there are also some boxplots displaying the
                    distribution of the amount of matches the players go without scoring. Due to Lionel Messi scoring earlier in his
                    career he seems like a more consistent player overall, however from the heatmaps we can see the two players are
                    comparable.''', style = {'backgroundColor' : '#222831', 'display': 'inline-block', 'verticalAlign': 'top',
                                             "width": "100%", "color": "white", 'fontSize': 14}),

                    html.Div(html.H4("Average Matches Played Without Scoring a Goal"), style = {'text-align': 'center', 'font-weight': 'bold', 'display': 'inline-block',
                                                                        'verticalAlign': 'top', 'width': '100%', 'backgroundColor' : '#222831', "color": 'white'}),

                    html.Div(html.H5("Lionel Messi: {}".format(messi_average_cummulative_games_with_no_goals)),
                             style = {'text-align': 'center', 'font-weight': 'bold', 'display': 'inline-block',
                                     'verticalAlign': 'top', 'width': '50%', 'backgroundColor' : '#222831', "color": 'white'}),
                    html.Div(html.H5("Cristiano Ronaldo: {}".format(ronaldo_average_cummulative_games_with_no_goals)),
                             style = {'text-align': 'center', 'font-weight': 'bold', 'display': 'inline-block',
                                     'verticalAlign': 'top', 'width': '50%', 'backgroundColor' : '#222831', "color": 'white'}),

                    html.Div(dcc.Graph(id = "Messi no goals",
                                       figure = {"data": [go.Heatmap(z = messi["Games With no Goal"],
                                                                     x = messi["Dates"],
                                                                     y = messi["Win Draw Loss"], zmin=0, zmax=35)],
                                                 "layout": go.Layout(title={'text': "Messi Matches Without Scoring",
                                                                            'x':0.5,
                                                                            },
                                                                    yaxis = {'categoryorder': 'array', 'categoryarray': ['L', 'D', 'W']},
                                                                    template = "plotly_dark", paper_bgcolor = '#222831'
                                                                            )}),
                                       style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),

                    html.Div(dcc.Graph(id = "ronaldo no goals",
                                       figure = {"data": [go.Heatmap(z = ronaldo["Games With no Goal"],
                                                                     x = ronaldo["Dates"],
                                                                     y = ronaldo["Win Draw Loss"])],
                                                 "layout": go.Layout(title={'text': "Ronaldo Matches Without Scoring",
                                                                            'x':0.5,
                                                                            },
                                                                    yaxis = {'categoryorder': 'array', 'categoryarray': ['L', 'D', 'W']},
                                                                    template = "plotly_dark", paper_bgcolor = '#222831'
                                                                            )}),
                                       style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),

                    html.Div(dcc.Graph(id = "Games Without a Goal Distribution",
                                       figure = {"data": [go.Box(x = ronaldo["Games With no Goal"],
                                                                 name="Ronaldo",
                                                                 jitter=0.3),
                                                          go.Box(x = messi["Games With no Goal"],
                                                                 name = "Messi",
                                                                 jitter = 0.3)],
                                                 "layout": go.Layout(title={'text': "Consecutive Matches Without a Goal Boxplots",
                                                                            'x':0.5},
                                                                    legend=dict(orientation="h", x=0.40, y=1.15),
                                                                    template = "plotly_dark", paper_bgcolor = '#222831')}),
                                       style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '100%'}),


                    html.Div(html.H3("Matches Played"), style = {'padding' : '0px',
                                                             'backgroundColor' : '#686868', 'display': 'inline-block', 'verticalAlign': 'top',
                                                              "width": "100%", "color": "gold"
                                                              }),

                    html.Div('''To see which player plays the most minutes in terms of not getting injured and play time, the average
                    minutes played per year is displayed below.''',
                    style = {'backgroundColor' : '#686868', 'display': 'inline-block', 'verticalAlign': 'top',
                             "width": "100%", "color": "white", 'fontSize': 14}),

                    html.Div(dcc.Graph(id = "Average Minutes per Year",
                                       figure = {"data": [go.Bar(x=messi_minutes_per_year["Dates"],
                                                                 y=messi_minutes_per_year["Minutes"],
                                                                 text=messi_minutes_per_year["Minutes"],
                                                                 textposition='auto',
                                                                 name = 'Messi'),
                                                          go.Bar(x=ronaldo_minutes_per_year["Dates"],
                                                                 y=ronaldo_minutes_per_year["Minutes"],
                                                                 text=ronaldo_minutes_per_year["Minutes"],
                                                                 textposition='auto',
                                                                 name = 'Ronaldo')],
                                                 "layout": go.Layout(title={'text': "Average Minutes Played per Year", 'x':0.5},
                                                                     legend=dict(orientation="h", x=0.40, y=1.15),
                                                                     template = "plotly_dark", paper_bgcolor = '#686868')}),
                                       style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '100%'}),

                    html.Div(html.H3("Player Match Availabilty"),
                    style = {'text-align': 'center', 'font-weight': 'bold', 'display': 'inline-block', 'verticalAlign': 'top',
                             'width': '100%', 'backgroundColor' : '#222831', "color": 'gold'}),

                    html.Div('''The availability of each player to play matches shows consistency in terms of a player being selected
                    or injury prone. Both players don't get injured for long periods of time and are always selected and fit to play.''',
                    style = {'backgroundColor' : '#222831', 'display': 'inline-block', 'verticalAlign': 'top',
                             "width": "100%", "color": "white", 'fontSize': 14}),

                    html.Div(dcc.Graph(id = "Messi Matches Played",
                                       figure = {"data": [go.Pie(labels = list(messi["Played"].unique()),
                                                                 values = messi_played,
                                                                 textinfo = 'label+percent',
                                                                 insidetextorientation = 'radial')],
                                                 "layout": go.Layout(title={'text': "Messi's Match Availabilty",
                                                                            'x':0.5}, template = "plotly_dark", paper_bgcolor = '#222831')}),
                                       style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),

                    html.Div(dcc.Graph(id = "Ronaldo Matches Played",
                                       figure = {"data": [go.Pie(labels = list(ronaldo["Played"].unique()),
                                                                 values = ronaldo_played,
                                                                 textinfo = 'label+percent',
                                                                 insidetextorientation = 'radial')],
                                                 "layout": go.Layout(title={'text': "Ronaldo's Match Availabilty",
                                                                            'x':0.5}, template = "plotly_dark", paper_bgcolor = '#222831')}),
                                       style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'})

                            ], style = {'text-align': 'center'})

########################################### Callbacks ###################################################
