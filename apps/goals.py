import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import datetime
import pathlib
from app import app
import plotly.io as pio
pio.templates.default = "plotly_dark"

########################################### Data ###################################################
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

messi = pd.read_excel(DATA_PATH.joinpath("messi clean.xlsx"))
ronaldo = pd.read_excel(DATA_PATH.joinpath("ronaldo clean.xlsx"))

########################################### Bar Charts
messi_gen_comps = pd.DataFrame(messi.groupby(['General Competition'])['Goals'].sum())
messi_gen_comps.reset_index(inplace = True, drop = False)
messi_gen_comps.sort_values(by = "Goals", inplace = True, ascending = True)

messi_gen_comps_games = pd.DataFrame(messi.groupby(['General Competition'])['Played'].count())
messi_gen_comps_games.reset_index(inplace = True, drop = False)
messi_gen_comps_games.sort_values(by = "Played", inplace = True, ascending = True)

messi_goals = messi_gen_comps["Goals"].values
messi_games = messi_gen_comps_games["Played"].values
messi_goals_per_game = messi_goals/messi_games
messi_goals_per_game = messi_goals_per_game.tolist()
messi_goals_per_game = [round(x, 2) for x in messi_goals_per_game]

ronaldo_gen_comps = pd.DataFrame(ronaldo.groupby(['General Competition'])['Goals'].sum())
ronaldo_gen_comps.reset_index(inplace = True, drop = False)
ronaldo_gen_comps.sort_values(by = "Goals", inplace = True, ascending = True)

ronaldo_gen_comps_games = pd.DataFrame(ronaldo.groupby(['General Competition'])['Played'].count())
ronaldo_gen_comps_games.reset_index(inplace = True, drop = False)
ronaldo_gen_comps_games.sort_values(by = "Played", inplace = True, ascending = True)

ronaldo_goals = ronaldo_gen_comps["Goals"].values
ronaldo_games = ronaldo_gen_comps_games["Played"].values
ronaldo_goals_per_game = ronaldo_goals/ronaldo_games
ronaldo_goals_per_game = ronaldo_goals_per_game.tolist()
ronaldo_goals_per_game = [round(x, 2) for x in ronaldo_goals_per_game]

# Goals per Year
goals_per_year_messi = messi.groupby(messi['Dates'].dt.year)['Goals'].agg(['sum'])
goals_per_year_messi["Player"] = "Lionel Messi"
goals_per_year_messi.reset_index(inplace = True, drop = False)
goals_per_year_ronaldo = ronaldo.groupby(ronaldo['Dates'].dt.year)['Goals'].agg(['sum'])
goals_per_year_ronaldo["Player"] = "Cristiano Ronaldo"
goals_per_year_ronaldo.reset_index(inplace = True, drop = False)

goals_per_year = pd.concat([goals_per_year_messi, goals_per_year_ronaldo])
goals_per_year.reset_index(inplace = True, drop = True)
goals_per_year_figure = px.scatter(data_frame = goals_per_year,
                                    x="Dates",
                                    y="sum",
                                    labels={
                                             "Dates": "Date",
                                             "sum": "Goals"
                                         },
                                    size = "sum",
                                    color = "Player",
                                    title = "Goals Scored per Year").update(layout=dict(title=dict(x=0.5),
                                                                                        paper_bgcolor="#686868",
                                                                                        legend=dict(
                                                                                            orientation="h",
                                                                                            yanchor="bottom",
                                                                                            y=1.02,
                                                                                            xanchor="center",
                                                                                            x=0.5
                                                                                        )))
########################################### Dropdown Options ###################################################
messi_teams = []
for team in messi["Squad"].unique():
    messi_teams.append({"label": str(team), "value": team})

ronaldo_teams = []
for team in ronaldo["Squad"].unique():
    ronaldo_teams.append({"label": str(team), "value": team})

goal_or_assist = [{"label": 'Goal', "value": 'Goal'}, {"label": 'Assist', "value": 'Assist'}]

########################################### Application ###################################################
layout = html.Div([ html.Div(html.H1("Goals"), style = {'padding' : '0px',
                                     'backgroundColor' : '#181818', 'display': 'inline-block', 'verticalAlign': 'top',
                                      "width": "100%", "color": "gold"
                                     }),

                    html.Div(html.H3("Goals Scored"), style = {'padding' : '0px',
                                                             'backgroundColor' : '#686868', 'display': 'inline-block', 'verticalAlign': 'top',
                                                              "width": "100%", "color": "gold"
                                                              }),

                    html.Div('''To compare the goals scored by both players, it is important to make comparisons by cumulative goals
                    scored over time, number of goals scored in a calendar year, and in terms of goals per game split up by competition and
                    number of goals by competition.''', style = {'backgroundColor' : '#686868', 'display': 'inline-block', 'verticalAlign': 'top',
                                                                                    "width": "100%", "color": "white", 'fontSize': 14}),

                    html.Div(dcc.Graph(id = "goal graphs",
                                       figure = {"data": [go.Scatter(x=messi["Dates"], y=messi["Cummulative Goals"], name = "Messi"),
                                                        go.Scatter(x=ronaldo["Dates"], y=ronaldo["Cummulative Goals"], name="Ronaldo")],
                                               "layout": go.Layout(title={'text': "Cumulative Goals Scored Over Time", 'x':0.5},
                                                                   xaxis_title="Date",
                                                                   yaxis_title="Cumulative Goals",
                                                                   legend=dict(orientation="h", x=0.27, y=1.15),
                                                                   template = "plotly_dark",
                                                                   paper_bgcolor = '#686868')}),
                                       style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),

                    html.Div(dcc.Graph(id = "goal graphs",
                                       figure = goals_per_year_figure),
                                       style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),

                    html.Div(dcc.Graph(id = "messi games general",
                                       figure = {"data": [go.Bar(x=messi_gen_comps_games["General Competition"], y=messi_goals_per_game, text=messi_goals_per_game,
                                                                 textposition='auto', name = 'Messi'),
                                                         go.Bar(x=ronaldo_gen_comps_games["General Competition"], y=ronaldo_goals_per_game, text=ronaldo_goals_per_game,
                                                                  textposition='auto', name = 'Ronaldo')],
                                                 "layout": go.Layout(title={'text': "Goals per Game by Competition Type", 'x':0.5},
                                                                     xaxis = {'categoryorder':'array',
                                                                              'categoryarray': ['World Cup', 'Friendlies', 'International Tournaments',
                                                                                              'League Cups', 'Champions League', 'League']},
                                                                     xaxis_title="Competition",
                                                                     yaxis_title="Ratio",
                                                                     legend=dict(orientation="h", x=0.27, y=1.15),
                                                                     template = "plotly_dark",
                                                                     paper_bgcolor = '#686868')}),
                                       style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),

                    html.Div(dcc.Graph(id = "messi goals scored by comp",
                                       figure = {"data": [go.Bar(y=messi_gen_comps["Goals"], x=messi_gen_comps["General Competition"], text=messi_gen_comps["Goals"],
                                                                 textposition='auto', name = 'Messi'),
                                                          go.Bar(y=ronaldo_gen_comps["Goals"], x=ronaldo_gen_comps["General Competition"], text=ronaldo_gen_comps["Goals"],
                                                                 textposition='auto', name = 'Ronaldo')],
                                                 "layout": go.Layout(title={'text': "Goals Scored by Competition Type", 'x':0.5},
                                                                     xaxis_title="Competition",
                                                                     yaxis_title="Goals",
                                                                     legend=dict(orientation="h", x=0.27, y=1.15),
                                                                     template = "plotly_dark",
                                                                     paper_bgcolor = '#686868')}),
                                       style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),

                    html.Div(html.H3("Number of Goals Scored per Match Outcome"), style = {'padding' : '0px',
                                                             'backgroundColor' : '#222831', 'display': 'inline-block', 'verticalAlign': 'top',
                                                              "width": "100%", "color": "gold"
                                                             }),

                    html.Div('''The heat maps give a visual representation of how important the goals are that each players scores. Overall you
                    can see that usually when either player doesn't score their teams either draw or lose compared to when they do score.
                    On the Y-axis W means Win, D means Draw and L means Loss.''',
                    style = {'backgroundColor' : '#222831', 'display': 'inline-block', 'verticalAlign': 'top',
                                                                                    "width": "100%", "color": "white", 'fontSize': 14}),

                    html.Div(dcc.Graph(id = "cummulative goals scored messi",
                                       figure = {"data": [go.Heatmap(z = messi["Goals"],
                                                                     x = messi["Dates"],
                                                                     y = messi["Win Draw Loss"],
                                                                     colorbar=dict(title="Goals"))],
                                                 "layout": go.Layout(title={'text': "Messi Match Outcomes Over Time",
                                                                            'x':0.5
                                                                            },
                                                                     xaxis_title="Date",
                                                                     yaxis_title="Outcome",
                                                                    template= "plotly_dark",
                                                                    paper_bgcolor = '#222831',
                                                                    yaxis = {'categoryorder': 'array', 'categoryarray': ['L', 'D', 'W']}

                                                                            )}),
                                       style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),

                    html.Div(dcc.Graph(id = "cummulative goals scored ronaldo",
                                       figure = {"data": [go.Heatmap(z = ronaldo["Goals"],
                                                                     x = ronaldo["Dates"],
                                                                     y = ronaldo["Win Draw Loss"],
                                                                     colorbar=dict(title="Goals"))],
                                                 "layout": go.Layout(title={'text': "Ronaldo Match Outcomes Over Time",
                                                                            'x':0.5},
                                                                     xaxis_title="Date",
                                                                     yaxis_title="Outcome",
                                                                     template= "plotly_dark",
                                                                    paper_bgcolor='#222831',
                                                                    yaxis = {'categoryorder': 'array', 'categoryarray': ['L', 'D', 'W']}

                                                                            )}),
                                       style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),


                    html.Div(html.H3("Probability of Winning Given Contribution"), style = {'padding' : '0px',
                                                             'backgroundColor' : '#686868', 'display': 'inline-block', 'verticalAlign': 'top',
                                                              "width": "100%", "color": "gold"}),

                    html.Div('''The bar charts represent the probability of each player's teams winning (past and present teams) given their
                    contribution types, whether it's a goal, an assist or both. This shows how important their contributions are to their teams.''',
                    style = {'backgroundColor' : '#686868', 'display': 'inline-block', 'verticalAlign': 'top',
                                                                                    "width": "100%", "color": "white", 'fontSize': 14}),

                    html.Div(html.Label(["Contribution Type:"]), style = {'text-align': 'center', 'font-weight': 'bold','display': 'inline-block',
                                                                          'verticalAlign': 'top', 'width': '100%', 'backgroundColor' : '#686868', "color": 'white'}),
                    html.Div(dcc.Dropdown(id = "impact_type",
                                         options=goal_or_assist,
                                         value=["Goal", "Assist"],
                                         multi = True), style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '100%'}),

                    html.Div(html.Label(["Messi's Teams:"]), style = {'text-align': 'center', 'font-weight': 'bold','display': 'inline-block',
                                                                      'verticalAlign': 'top', 'width': '50%', 'backgroundColor' : '#686868', "color": 'white'}),
                    html.Div(html.Label(["Ronaldo's Teams:"]), style = {'text-align': 'center', 'font-weight': 'bold', 'display': 'inline-block',
                                                                        'verticalAlign': 'top', 'width': '50%', 'backgroundColor' : '#686868', "color": 'white'}),

                    html.Div(dcc.Dropdown(id = "messi_probability_dropdown",
                                         options=messi_teams,
                                         value=['Barcelona', "Argentina"],
                                         multi = True), style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),

                    html.Div(dcc.Dropdown(id = "ronaldo_probability_dropdown",
                                         options=ronaldo_teams,
                                         value=['Sporting CP', 'Manchester Utd', 'Portugal', 'Real Madrid', 'Juventus'],
                                         multi = True), style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),

                    html.Div(dcc.Graph(id = "messi_probability_barplot", figure = {}), style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),

                    html.Div(dcc.Graph(id = "ronaldo_probability_barplot", figure = {}), style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'})



                            ], style = {'text-align': 'center'})
########################################### Callbacks ###################################################
# Messi Probability Bar Chart
@app.callback(Output("messi_probability_barplot", 'figure'),
              [Input('messi_probability_dropdown', 'value'),
               Input('impact_type', 'value')])
def set_card_type_options(teams, contribution_type):
    messi_probs = []
    for value in teams:
        if contribution_type == ["Goal", "Assist"] or contribution_type == ["Assist", "Goal"]:
            rows_messi = messi[(messi['Squad'].isin([value])) & (messi["Minutes"] > 0)]
            filtered_scored_messi= rows_messi[(rows_messi["Win Draw Loss"].isin(["W"])) & (rows_messi["Goals"] > 0) | (rows_messi["Assists"] > 0)]
            win_filtered_scored_messi = round(len(filtered_scored_messi)/len(rows_messi), 4)
            win_filtered_scored_messi = win_filtered_scored_messi * 100
            messi_probs.append(win_filtered_scored_messi)

        if contribution_type == ["Goal"]:
            rows_messi = messi[(messi['Squad'].isin([value])) & (messi["Minutes"] > 0)]
            filtered_scored_messi= rows_messi[(rows_messi["Win Draw Loss"].isin(["W"])) & (rows_messi["Goals"] > 0)]
            win_filtered_scored_messi = round(len(filtered_scored_messi)/len(rows_messi), 4)
            win_filtered_scored_messi = win_filtered_scored_messi * 100
            messi_probs.append(win_filtered_scored_messi)

        if contribution_type == ["Assist"]:
            rows_messi = messi[(messi['Squad'].isin([value])) & (messi["Minutes"] > 0)]
            filtered_scored_messi= rows_messi[(rows_messi["Win Draw Loss"].isin(["W"])) & (rows_messi["Assists"] > 0)]
            win_filtered_scored_messi = round(len(filtered_scored_messi)/len(rows_messi), 4)
            win_filtered_scored_messi = win_filtered_scored_messi * 100
            messi_probs.append(win_filtered_scored_messi)

    traces = []
    i = 0
    for value in messi_probs:
        traces.append(go.Bar(x=[teams[i]], y=[value], name = teams[i]))
        i = i + 1

    return {"data": traces, "layout": go.Layout(title={'text': "Lionel Messi", 'x':0.5},
                                                xaxis_title="Teams",
                                                yaxis_title="Percent",
                                                yaxis=dict(range=[0, 100]),
                                                template = "plotly_dark",
                                                paper_bgcolor = '#686868')}

# Ronaldo Probability Bar Chart
@app.callback(Output("ronaldo_probability_barplot", 'figure'),
              [Input('ronaldo_probability_dropdown', 'value'),
               Input('impact_type', 'value')])
def set_card_type_options(teams, contribution_type):
    ronaldo_probs = []
    for value in teams:
        if contribution_type == ["Goal", "Assist"] or contribution_type == ["Assist", "Goal"]:
            rows_ronaldo = ronaldo[(ronaldo['Squad'].isin([value])) & (ronaldo["Minutes"] > 0)]
            filtered_scored_ronaldo= rows_ronaldo[(rows_ronaldo["Win Draw Loss"].isin(["W"])) & (rows_ronaldo["Goals"] > 0) | (rows_ronaldo["Assists"] > 0)]
            win_filtered_scored_ronaldo = round(len(filtered_scored_ronaldo)/len(rows_ronaldo),4)
            win_filtered_scored_ronaldo = win_filtered_scored_ronaldo * 100
            ronaldo_probs.append(win_filtered_scored_ronaldo)

        if contribution_type == ["Goal"]:
            rows_ronaldo = ronaldo[(ronaldo['Squad'].isin([value])) & (ronaldo["Minutes"] > 0)]
            filtered_scored_ronaldo= rows_ronaldo[(rows_ronaldo["Win Draw Loss"].isin(["W"])) & (rows_ronaldo["Goals"] > 0)]
            win_filtered_scored_ronaldo = round(len(filtered_scored_ronaldo)/len(rows_ronaldo),4)
            win_filtered_scored_ronaldo = win_filtered_scored_ronaldo * 100
            ronaldo_probs.append(win_filtered_scored_ronaldo)

        if contribution_type == ["Assist"]:
            rows_ronaldo = ronaldo[(ronaldo['Squad'].isin([value])) & (ronaldo["Minutes"] > 0)]
            filtered_scored_ronaldo= rows_ronaldo[(rows_ronaldo["Win Draw Loss"].isin(["W"])) & (rows_ronaldo["Assists"] > 0)]
            win_filtered_scored_ronaldo = round(len(filtered_scored_ronaldo)/len(rows_ronaldo),4)
            win_filtered_scored_ronaldo = win_filtered_scored_ronaldo * 100
            ronaldo_probs.append(win_filtered_scored_ronaldo)

    traces = []
    i = 0
    for value in ronaldo_probs:
        traces.append(go.Bar(x=[teams[i]], y=[value], name = teams[i]))
        i = i + 1

    return {"data": traces, "layout": go.Layout(title={'text': "Cristiano Ronaldo", 'x':0.5},
                                                xaxis_title="Teams",
                                                yaxis_title="Percent",
                                                yaxis=dict(range=[0, 100]),
                                                template = "plotly_dark",
                                                paper_bgcolor = '#686868')}
