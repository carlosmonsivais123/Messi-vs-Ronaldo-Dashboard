import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import datetime
import pathlib
import plotly.express as px
from app import app
import plotly.io as pio
pio.templates.default = "plotly_dark"

########################################### Data ###################################################
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

messi = pd.read_excel(DATA_PATH.joinpath("messi clean.xlsx"))
ronaldo = pd.read_excel(DATA_PATH.joinpath("ronaldo clean.xlsx"))

words = ['Matchweek ', 'Friendlies (M)', 'Third-place match']

rounds_messi_new = list(messi["Round"].unique())
for value in words:
    rounds_messi_new = [x for x in rounds_messi_new if value not in x]
clutch_messi = messi[messi['Round'].isin(rounds_messi_new)]
clutch_messi = clutch_messi[['Dates', 'Result', 'Win Draw Loss', 'Competition',
                             'General Competition', 'Round', 'Venue', 'Squad', 'Opponent',
                             'Game Started', 'Minutes', 'Played', 'Goals', "Assists"]]
clutch_messi["Player"] = "Lionel Messi"

rounds_ronaldo_new = list(ronaldo["Round"].unique())
for value in words:
    rounds_ronaldo_new = [x for x in rounds_ronaldo_new if value not in x]
clutch_ronaldo = ronaldo[ronaldo['Round'].isin(rounds_ronaldo_new)]
clutch_ronaldo = clutch_ronaldo[['Dates', 'Result', 'Win Draw Loss', 'Competition',
                                 'General Competition', 'Round', 'Venue', 'Squad', 'Opponent',
                                 'Game Started', 'Minutes', 'Played', 'Goals', "Assists"]]
clutch_ronaldo["Player"] = "Cristiano Ronaldo"

clutch = pd.concat([clutch_messi, clutch_ronaldo])
clutch.reset_index(inplace = True, drop = True)

clutch["Contributions"] = clutch["Goals"] + clutch["Assists"]
clutch["All Tournaments"] = "All Tournaments"
clutch["All Rounds"] = "All Rounds"

# Dropping Supercopa de Espana, not what I consider a tournament.
clutch = clutch[clutch.Competition != 'Supercopa de España'].copy()
clutch.reset_index(inplace = True, drop = True)

# UEFA Super Cup is techically a final.
clutch['Round'].replace('UEFA Super Cup', 'Final', inplace = True)
clutch['Round'].replace('Supercoppa Italiana', 'Final', inplace = True)

########################################### Dropdown Options ###################################################
general_comp_drop = []
for comp in clutch["General Competition"].unique():
    general_comp_drop.append({"label": str(comp), "value": comp})
all_value = {"label": "All Tournaments", "value": "All Tournaments"}
general_comp_drop = [all_value] + general_comp_drop

specific_comp_drop = []
for comp in clutch["Competition"].unique():
    specific_comp_drop.append({"label": str(comp), "value": comp})
all_value_spec = {"label": "All Tournaments", "value": "All Tournaments"}
specific_comp_drop = [all_value_spec] + specific_comp_drop
########################################## Application ###################################################
layout = html.Div([
                    html.Div(html.H1("Tournaments"), style = {'padding' : '0px',
                                                                'backgroundColor' : '#181818', 'display': 'inline-block', 'verticalAlign': 'top',
                                                                "width": "100%", "color": "gold"}),

                    html.Div(html.H3("Player Tournament Statistics"), style = {'padding' : '0px',
                                                             'backgroundColor' : '#686868', 'display': 'inline-block', 'verticalAlign': 'top',
                                                              "width": "100%", "color": "gold"
                                                             }),

                    html.Div('''In order to measure how well a player does in crucial situations, and more specifically in a tournament setting,
                    scroll through the filters below to choose which competition you want to compare the player statistics with.''',
                    style = {'backgroundColor' : '#686868', 'display': 'inline-block', 'verticalAlign': 'top',
                             "width": "100%", "color": "white", 'fontSize': 14}),

                    html.Div(html.Label(["General Comepetition Type:"]), style = {'text-align': 'center', 'font-weight': 'bold', 'display': 'inline-block',
                                                                          'verticalAlign': 'top', 'width': '50%', 'backgroundColor' : '#686868', "color": 'white'}),

                    html.Div(html.Label(["Specific Comepeition Type:"]), style = {'text-align': 'center', 'font-weight': 'bold', 'display': 'inline-block',
                                                                        'verticalAlign': 'top', 'width': '50%', 'backgroundColor' : '#686868', "color": 'white'}),
                    html.Div(dcc.Dropdown(id = "general_comp_dropdown",
                                         options=general_comp_drop,
                                         value="All Tournaments",
                                         multi = False), style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),

                    html.Div(dcc.Dropdown(id = "specific_comp_dropdown",
                                         options=specific_comp_drop,
                                         value="All Tournaments",
                                         multi = False), style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),

                    html.Div(
                            dcc.Graph(id = "competition_table"),
                                      style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '100%'}
                                            ),

                    html.Div(id = "Title Text", style = {'padding' : '0px',
                                                             'backgroundColor' : '#222831', 'display': 'inline-block', 'verticalAlign': 'top',
                                                              "width": "100%", "color": "gold"
                                                             }),

                    html.Div('''Using the filters above you can see how well the player's teams did in each stage of the tournament filter selected.
                    With this in mind, even though it is a team sport, these two players should be able to affect games in a big way with their talents,
                    showing their value.''',
                    style = {'backgroundColor' : '#222831', 'display': 'inline-block', 'verticalAlign': 'top',
                             "width": "100%", "color": "white", 'fontSize': 14}),

                    html.Div(
                            dcc.Graph(id = "funnel messi"),
                                      style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}
                                            ),

                    html.Div(
                            dcc.Graph(id = "funnel ronaldo"),
                                      style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}
                                            ),

                    html.Div(html.H3("Contributions per Finals"), style = {'padding' : '0px',
                                                             'backgroundColor' : '#686868', 'display': 'inline-block', 'verticalAlign': 'top',
                                                              "width": "100%", "color": "gold"
                                                             }),

                    html.Div('''Using the dropdown filters below, you can see the number of contributions by type and the outcome in the tournament
                    level. This is used to see a connection between the number of contributions in the tournament stage and the outcome to see the
                    effects each player has in these crucial moments.''',
                    style = {'backgroundColor' : '#686868', 'display': 'inline-block', 'verticalAlign': 'top',
                             "width": "100%", "color": "white", 'fontSize': 14}),

                    html.Div(html.Label(["Contribution Type:"]), style = {'text-align': 'center', 'font-weight': 'bold', 'display': 'inline-block',
                                                                          'verticalAlign': 'top', 'width': '50%', 'backgroundColor' : '#686868', "color": 'white'}),

                    html.Div(html.Label(["Tournament Round:"]), style = {'text-align': 'center', 'font-weight': 'bold', 'display': 'inline-block',
                                                                        'verticalAlign': 'top', 'width': '50%', 'backgroundColor' : '#686868', "color": 'white'}),

                    html.Div(dcc.Dropdown(
                        id='contrib type final',
                        options=[
                            {'label': 'All Contributions', 'value': 'Contributions'},
                            {'label': 'Goals', 'value': 'Goals'},
                            {'label': 'Assists', 'value': 'Assists'}
                        ],
                        value='Contributions'
                    ), style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),


                    html.Div(dcc.Dropdown(
                        id='contrib round',
                        options=[
                            {'label': 'Final', 'value': 'Final'},
                            {'label': 'Semi-finals', 'value': 'Semi-finals'},
                            {'label': 'Quarter-finals', 'value': 'Quarter-finals'},
                            {'label': 'Round of 16', 'value': 'Round of 16'},
                            {'label': 'Group stage', 'value': 'Group stage'}
                        ],
                        value='Final'
                    ), style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}),

                    html.Div(
                            dcc.Graph(id = "finals conts"),
                                      style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '100%'}),

                   html.Div(dcc.Graph(id = "finals_table"),
                                      style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '100%'}),



                            ], style = {'text-align': 'center'})

########################################### Callbacks ###################################################
@app.callback(Output('specific_comp_dropdown', 'options'),
              [Input('general_comp_dropdown', 'value')])
def specific_comp(selected_competition):
    filtered_df = clutch[clutch["General Competition"] == selected_competition]
    filtered_df.reset_index(drop = True, inplace = True)
    specific_comp_drop = []
    for comp in filtered_df["Competition"].unique():
        specific_comp_drop.append({"label": str(comp), "value": comp})

    all_value_spec = {"label": "All Tournaments", "value": "All Tournaments"}
    specific_comp_drop = [all_value_spec] + specific_comp_drop

    return specific_comp_drop

@app.callback(Output('competition_table', 'figure'),
              [Input('general_comp_dropdown', 'value'),
               Input('specific_comp_dropdown', 'value')])
def set_card_type_options(general_comp, specific_comp):
    if general_comp == "All Tournaments" and specific_comp == "All Tournaments":
        filtered_df = clutch.copy()

        ronaldo_table = []
        messi_table = []

        value_names = ["Win Percentage", "Draw Percentage", "Loss Percentage", "Wins", "Draws", "Losses", "Games Played",
                       "Goals", "Assists", "Goals per Game", "Assists per Game", "Contributions per Game (Goals + Assists)"]

    ###### Win % #######
        wdl_table = filtered_df[["Win Draw Loss", "Player", "Goals"]].groupby(["Player", "Win Draw Loss"]).count().T
        played = filtered_df[["Dates", "Player"]].groupby(["Player"]).count().T

        ronaldo_table.append("{}%".format(round(wdl_table["Cristiano Ronaldo"]["W"].tolist()[0] / played["Cristiano Ronaldo"].tolist()[0] * 100, 2)))
        messi_table.append("{}%".format(round(wdl_table["Lionel Messi"]["W"].tolist()[0] / played["Lionel Messi"].tolist()[0] * 100, 2)))

    ###### Draw % #######
        ronaldo_table.append("{}%".format(round(wdl_table["Cristiano Ronaldo"]["D"].tolist()[0] / played["Cristiano Ronaldo"].tolist()[0] * 100, 2)))
        messi_table.append("{}%".format(round(wdl_table["Lionel Messi"]["D"].tolist()[0] / played["Lionel Messi"].tolist()[0], 2) * 100))

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
        goals = filtered_df[["Goals", "Player"]].groupby(["Player"]).sum().T
        ronaldo_table.append(goals["Cristiano Ronaldo"].tolist()[0])
        messi_table.append(goals["Lionel Messi"].tolist()[0])

    ###### Assists #######
        assists = filtered_df[["Assists", "Player"]].groupby(["Player"]).sum().T
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

        traces = []

        traces.append(go.Table(
                    header=dict(values=list(["", "Lionel Messi", "Cristiano Ronaldo"]),
                                fill_color='#222831',
                                line_color='white',
                                font=dict(color='white', size=13),
                                align='center'),
                    cells=dict(values=[value_names, messi_table, ronaldo_table]))

            )
        return {"data": traces, "layout": go.Layout(title={'text': "Player Records in {}".format(specific_comp),
                                   'x':0.5},
                            height = 450,
                            template= "plotly_dark",
                            paper_bgcolor = '#686868')}

    else:
        if general_comp != "All Tournaments" and specific_comp != "All Tournaments":
            filtered_df = clutch[(clutch["General Competition"] == general_comp) & (clutch["Competition"] == specific_comp)]

        elif general_comp != "All Tournaments" and specific_comp == "All Tournaments":
            filtered_df = clutch[(clutch["General Competition"] == general_comp)]

        elif general_comp == "All Tournaments" and specific_comp != "All Tournaments":
            filtered_df = clutch[clutch["Competition"] == specific_comp]

        ronaldo_table = []
        messi_table = []

        value_names = ["Win Percentage", "Draw Percentage", "Loss Percentage", "Wins", "Draws", "Losses", "Games Played",
                       "Goals", "Assists", "Goals per Game", "Assists per Game", "Contributions per Game (Goals + Assists)"]

    ###### Win % #######
        wdl_table = filtered_df[["Win Draw Loss", "Player", "Goals"]].groupby(["Player", "Win Draw Loss"]).count().T
        played = filtered_df[["Dates", "Player"]].groupby(["Player"]).count().T

        try:
            ronaldo_table.append("{}%".format(round(wdl_table["Cristiano Ronaldo"]["W"].tolist()[0] / played["Cristiano Ronaldo"].tolist()[0] * 100, 2)))
        except:
            ronaldo_table.append("NaN")

        try:
            messi_table.append("{}%".format(round(wdl_table["Lionel Messi"]["W"].tolist()[0] / played["Lionel Messi"].tolist()[0] * 100, 2)))
        except:
            messi_table.append("NaN")

    ###### Draw % #######
        try:
            ronaldo_table.append("{}%".format(round(wdl_table["Cristiano Ronaldo"]["D"].tolist()[0] / played["Cristiano Ronaldo"].tolist()[0] * 100, 2)))
        except:
            ronaldo_table.append("NaN")

        try:
            messi_table.append("{}%".format(round(wdl_table["Lionel Messi"]["D"].tolist()[0] / played["Lionel Messi"].tolist()[0] * 100, 2)))
        except:
            messi_table.append("NaN")

    ###### Loss % #######
        try:
            ronaldo_table.append("{}%".format(round(wdl_table["Cristiano Ronaldo"]["L"].tolist()[0] / played["Cristiano Ronaldo"].tolist()[0] * 100, 2)))
        except:
            ronaldo_table.append("NaN")

        try:
            messi_table.append("{}%".format(round(wdl_table["Lionel Messi"]["L"].tolist()[0] / played["Lionel Messi"].tolist()[0] * 100, 2)))
        except:
            messi_table.append("NaN")

    ###### WDL #######
        try:
            ronaldo_table.append(wdl_table["Cristiano Ronaldo"]["W"].tolist()[0])
        except:
            ronaldo_table.append("NaN")
        try:
            ronaldo_table.append(wdl_table["Cristiano Ronaldo"]["D"].tolist()[0])
        except:
            ronaldo_table.append("NaN")
        try:
            ronaldo_table.append(wdl_table["Cristiano Ronaldo"]["L"].tolist()[0])
        except:
            ronaldo_table.append("NaN")

        try:
            messi_table.append(wdl_table["Lionel Messi"]["W"].tolist()[0])
        except:
            messi_table.append("NaN")
        try:
            messi_table.append(wdl_table["Lionel Messi"]["D"].tolist()[0])
        except:
            messi_table.append("NaN")
        try:
            messi_table.append(wdl_table["Lionel Messi"]["L"].tolist()[0])
        except:
            messi_table.append("NaN")

    ###### Played #######
        try:
            ronaldo_table.append(played["Cristiano Ronaldo"].tolist()[0])
        except:
            ronaldo_table.append("NaN")
        try:
            messi_table.append(played["Lionel Messi"].tolist()[0])
        except:
            messi_table.append("NaN")

    ###### Goals #######
        goals = filtered_df[["Goals", "Player"]].groupby(["Player"]).sum().T
        try:
            ronaldo_table.append(goals["Cristiano Ronaldo"].tolist()[0])
        except:
            ronaldo_table.append("NaN")
        try:
            messi_table.append(goals["Lionel Messi"].tolist()[0])
        except:
            messi_table.append("NaN")

    ###### Assists #######
        assists = filtered_df[["Assists", "Player"]].groupby(["Player"]).sum().T
        try:
            ronaldo_table.append(assists["Cristiano Ronaldo"].tolist()[0])
        except:
            ronaldo_table.append("NaN")

        try:
            messi_table.append(assists["Lionel Messi"].tolist()[0])
        except:
            messi_table.append("NaN")

    ###### Goals per Game #######
        try:
            ronaldo_table.append(round((goals["Cristiano Ronaldo"].tolist()[0]) / played["Cristiano Ronaldo"].tolist()[0], 2))
        except:
            ronaldo_table.append("NaN")

        try:
            messi_table.append(round((goals["Lionel Messi"].tolist()[0]) / played["Lionel Messi"].tolist()[0], 2))
        except:
            messi_table.append("NaN")

    ###### Assists per Game #######
        try:
            ronaldo_table.append(round((assists["Cristiano Ronaldo"].tolist()[0]) / played["Cristiano Ronaldo"].tolist()[0], 2))
        except:
            ronaldo_table.append("NaN")

        try:
            messi_table.append(round((assists["Lionel Messi"].tolist()[0]) / played["Lionel Messi"].tolist()[0], 2))
        except:
            messi_table.append("NaN")


    ###### Contribution Per Game #######
        try:
            ronaldo_table.append(round((goals["Cristiano Ronaldo"].tolist()[0] + assists["Cristiano Ronaldo"].tolist()[0]) / played["Cristiano Ronaldo"].tolist()[0], 2))
        except:
            ronaldo_table.append("NaN")

        try:
            messi_table.append(round((goals["Lionel Messi"].tolist()[0] + assists["Lionel Messi"].tolist()[0]) / played["Lionel Messi"].tolist()[0], 2))
        except:
            messi_table.append("NaN")

        traces = []

        traces.append(go.Table(
                    header=dict(values=list(["", "Lionel Messi", "Cristiano Ronaldo"]),
                                fill_color='#222831',
                                line_color='white',
                                font=dict(color='white', size=13),
                                align='center'),
                    cells=dict(values=[value_names, messi_table, ronaldo_table]))

            )
        return {"data": traces, "layout": go.Layout(title={'text': "Player Records in {}".format(specific_comp),
                                   'x':0.5},
                            height = 450,
                            template= "plotly_dark",
                            paper_bgcolor = '#686868')}

@app.callback(Output('funnel messi', 'figure'),
              [Input('general_comp_dropdown', 'value')])
def specific_comp(selected_competition):
    if selected_competition == "All Tournaments":
        champ_leag = clutch[clutch["All Tournaments"] == selected_competition]
        category_orders2 = {"Round": ['Final', 'Semi-finals', 'Quarter-finals', 'Round of 16', 'Group stage', 'WCQ — CONMEBOL (M)'],
                            "Win Draw Loss": ["W", "D", "L"]}

        champ_leag.reset_index(drop = True, inplace = True)

        messi_game_count = champ_leag[champ_leag["Player"] == "Lionel Messi"]
        messi_wdl_games = messi_game_count.groupby(["Round", "Win Draw Loss"]).count()["Dates"]
        messi_wdl_games = pd.DataFrame(messi_wdl_games)
        messi_wdl_games.reset_index(inplace = True, drop = False)

        messi_played_games = messi_game_count.groupby(["Round", "Player"]).count()["Dates"]
        messi_played_games = pd.DataFrame(messi_played_games)
        messi_played_games.reset_index(inplace = True, drop = False)

        messi_wdl_games["Divide"] = messi_wdl_games['Round'].map(messi_played_games.set_index('Round')['Dates'])
        messi_wdl_games["Percent"] = round(messi_wdl_games['Dates']/messi_wdl_games['Divide'] * 100)

        percent_text = []
        for value in messi_wdl_games["Percent"]:
            percent_text.append("{}%".format(value))

        messi_wdl_games["Percent Text"] = percent_text

        fig = px.bar(messi_wdl_games, x="Percent", y="Round",
                     color='Win Draw Loss', orientation='h', title = "Lionel Messi",
                     text = "Percent Text", category_orders = category_orders2).update(layout=dict(title=dict(x=0.5),
                                                                                                   paper_bgcolor="#222831",
                                                                                                   legend=dict(
                                                                                                       orientation="h",
                                                                                                       yanchor="bottom",
                                                                                                       y=1.02,
                                                                                                       xanchor="center",
                                                                                                       x=0.45
                                                                                                   )))
        return fig

    else:
        champ_leag = clutch[clutch["General Competition"] == selected_competition]

        if selected_competition == "Champions League":
            champions_league_list = ['Group stage', 'Round of 16', 'Semi-finals', 'Quarter-finals','Final']
            champ_leag = champ_leag[champ_leag['Round'].isin(champions_league_list)]
            category_orders2 = {"Round": ['Final', 'Semi-finals', 'Quarter-finals', 'Round of 16', 'Group stage'],
                                "Win Draw Loss": ["W", "D", "L"]}

        elif selected_competition == "World Cup":
            category_orders2 = {"Round": ['Final', 'Semi-finals', 'Quarter-finals', 'Round of 16', 'Group stage'],
                                "Win Draw Loss": ["W", "D", "L"]}

        elif selected_competition == "International Tournaments":
            champions_league_list = ['Group stage', 'Round of 16', 'Semi-finals', 'Quarter-finals','Final', 'WCQ — CONMEBOL (M)']
            champ_leag = champ_leag[champ_leag['Round'].isin(champions_league_list)]
            category_orders2 = {"Round": ['Final', 'Semi-finals', 'Quarter-finals', 'Group stage', 'WCQ — CONMEBOL (M)'],
                                "Win Draw Loss": ["W", "D", "L"]}

        elif selected_competition == "League Cups":
            category_orders2 = {"Round": ['Final', 'Semi-finals', 'Quarter-finals', 'Round of 16', 'Group stage'],
                                "Win Draw Loss": ["W", "D", "L"]}

        champ_leag.reset_index(drop = True, inplace = True)

        messi_game_count = champ_leag[champ_leag["Player"] == "Lionel Messi"]
        messi_wdl_games = messi_game_count.groupby(["Round", "Win Draw Loss"]).count()["Dates"]
        messi_wdl_games = pd.DataFrame(messi_wdl_games)
        messi_wdl_games.reset_index(inplace = True, drop = False)

        messi_played_games = messi_game_count.groupby(["Round", "Player"]).count()["Dates"]
        messi_played_games = pd.DataFrame(messi_played_games)
        messi_played_games.reset_index(inplace = True, drop = False)

        messi_wdl_games["Divide"] = messi_wdl_games['Round'].map(messi_played_games.set_index('Round')['Dates'])
        messi_wdl_games["Percent"] = round(messi_wdl_games['Dates']/messi_wdl_games['Divide'] * 100)

        percent_text = []
        for value in messi_wdl_games["Percent"]:
            percent_text.append("{}%".format(value))

        messi_wdl_games["Percent Text"] = percent_text

        fig = px.bar(messi_wdl_games, x="Percent", y="Round",
                     color='Win Draw Loss', orientation='h', title = "Lionel Messi",
                     text = "Percent Text", category_orders = category_orders2).update(layout=dict(title=dict(x=0.5),
                                                                                                   paper_bgcolor="#222831",
                                                                                                   legend=dict(
                                                                                                       orientation="h",
                                                                                                       yanchor="bottom",
                                                                                                       y=1.02,
                                                                                                       xanchor="center",
                                                                                                       x=0.45
                                                                                                   )))
        return fig

@app.callback(Output('funnel ronaldo', 'figure'),
              [Input('general_comp_dropdown', 'value')])
def specific_comp(selected_competition):
    if selected_competition == "All Tournaments":
        champ_leag = clutch[clutch["All Tournaments"] == selected_competition]
        all_league_list = ['Group stage', 'Round of 16', 'Semi-finals', 'Quarter-finals','Final']
        champ_leag = champ_leag[champ_leag['Round'].isin(all_league_list)]
        category_orders2 = {"Round": ['Final', 'Semi-finals', 'Quarter-finals', 'Round of 16', 'Group stage'],
                            "Win Draw Loss": ["W", "D", "L"]}

        champ_leag.reset_index(drop = True, inplace = True)

        ronaldo_game_count = champ_leag[champ_leag["Player"] == "Cristiano Ronaldo"]
        ronaldo_wdl_games = ronaldo_game_count.groupby(["Round", "Win Draw Loss"]).count()["Dates"]
        ronaldo_wdl_games = pd.DataFrame(ronaldo_wdl_games)
        ronaldo_wdl_games.reset_index(inplace = True, drop = False)

        ronaldo_played_games = ronaldo_game_count.groupby(["Round", "Player"]).count()["Dates"]
        ronaldo_played_games = pd.DataFrame(ronaldo_played_games)
        ronaldo_played_games.reset_index(inplace = True, drop = False)

        ronaldo_wdl_games["Divide"] = ronaldo_wdl_games['Round'].map(ronaldo_played_games.set_index('Round')['Dates'])
        ronaldo_wdl_games["Percent"] = round(ronaldo_wdl_games['Dates']/ronaldo_wdl_games['Divide'] * 100)

        percent_text = []
        for value in ronaldo_wdl_games["Percent"]:
            percent_text.append("{}%".format(value))

        ronaldo_wdl_games["Percent Text"] = percent_text

        fig = px.bar(ronaldo_wdl_games, x="Percent", y="Round",
                     color='Win Draw Loss', orientation='h', title = "Cristiano Ronaldo",
                     text = "Percent Text", category_orders = category_orders2).update(layout=dict(title=dict(x=0.5),
                                                                                                   paper_bgcolor="#222831",
                                                                                                   legend=dict(
                                                                                                       orientation="h",
                                                                                                       yanchor="bottom",
                                                                                                       y=1.02,
                                                                                                       xanchor="center",
                                                                                                       x=0.45
                                                                                                   )))
        return fig

    else:
        champ_leag = clutch[clutch["General Competition"] == selected_competition]
        if selected_competition == "Champions League":
            champions_league_list = ['Group stage', 'Round of 16', 'Semi-finals', 'Quarter-finals','Final']
            champ_leag = champ_leag[champ_leag['Round'].isin(champions_league_list)]
            category_orders2 = {"Round": ['Final', 'Semi-finals', 'Quarter-finals', 'Round of 16', 'Group stage'],
                                "Win Draw Loss": ["W", "D", "L"]}

        if selected_competition == "World Cup":
            category_orders2 = {"Round": ['Final', 'Semi-finals', 'Quarter-finals', 'Round of 16', 'Group stage'],
                                "Win Draw Loss": ["W", "D", "L"]}

        if selected_competition == "International Tournaments":
            champions_league_list = ['Group stage', 'Round of 16', 'Semi-finals', 'Quarter-finals','Final']
            champ_leag = champ_leag[champ_leag['Round'].isin(champions_league_list)]
            category_orders2 = {"Round": ['Final', 'Semi-finals', 'Quarter-finals', 'Round of 16', 'Group stage'],
                                "Win Draw Loss": ["W", "D", "L"]}

        if selected_competition == "League Cups":
            category_orders2 = {"Round": ['Final', 'Semi-finals', 'Quarter-finals', 'Round of 16', 'Group stage'],
                                "Win Draw Loss": ["W", "D", "L"]}

        champ_leag.reset_index(drop = True, inplace = True)

        ronaldo_game_count = champ_leag[champ_leag["Player"] == "Cristiano Ronaldo"]
        ronaldo_wdl_games = ronaldo_game_count.groupby(["Round", "Win Draw Loss"]).count()["Dates"]
        ronaldo_wdl_games = pd.DataFrame(ronaldo_wdl_games)
        ronaldo_wdl_games.reset_index(inplace = True, drop = False)

        ronaldo_played_games = ronaldo_game_count.groupby(["Round", "Player"]).count()["Dates"]
        ronaldo_played_games = pd.DataFrame(ronaldo_played_games)
        ronaldo_played_games.reset_index(inplace = True, drop = False)

        ronaldo_wdl_games["Divide"] = ronaldo_wdl_games['Round'].map(ronaldo_played_games.set_index('Round')['Dates'])
        ronaldo_wdl_games["Percent"] = round(ronaldo_wdl_games['Dates']/ronaldo_wdl_games['Divide'] * 100)

        percent_text = []
        for value in ronaldo_wdl_games["Percent"]:
            percent_text.append("{}%".format(value))

        ronaldo_wdl_games["Percent Text"] = percent_text

        fig = px.bar(ronaldo_wdl_games, x="Percent", y="Round",
                     color='Win Draw Loss', orientation='h', title = "Cristiano Ronaldo",
                     text = "Percent Text", category_orders = category_orders2).update(layout=dict(title=dict(x=0.5),
                                                                                                   paper_bgcolor="#222831",
                                                                                                   legend=dict(
                                                                                                       orientation="h",
                                                                                                       yanchor="bottom",
                                                                                                       y=1.02,
                                                                                                       xanchor="center",
                                                                                                       x=0.45
                                                                                                   )))
        return fig

@app.callback(Output('Title Text', 'children'),
              [Input('general_comp_dropdown', 'value')])
def specific_comp(selected_value):
    return html.H3("Percentage of Games Won in {}".format(selected_value))

@app.callback(Output('finals conts', 'figure'),
              [Input('contrib type final', 'value'),
               Input('contrib round', 'value')])
def specific_comp(selected_contribution, selected_round):
    filtered_df = clutch[clutch["Round"] == "{}".format(selected_round)].copy()
    fig = px.line(filtered_df,
                     x="Dates",
                     y="{}".format(selected_contribution),
                     color = "Player",
                     facet_col = "General Competition",
                     facet_row = "Player",
                    text = "Win Draw Loss")
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_traces(textposition='top center')
    fig.update_layout(title_text="{}: {}".format(selected_contribution, selected_round),
                      title_x=0.45,
                      paper_bgcolor="#686868"
                      )

    return fig

@app.callback(Output('finals_table', 'figure'),
              [Input('contrib round', 'value')])
def set_card_type_options(specific_comp):
    all_final = clutch[(clutch["Round"] == "{}".format(specific_comp))].copy()

    ronaldo_table_final = []
    messi_table_final = []

    value_names_final = ["Win Percentage", "Loss Percentage", "Wins", "Losses", "Games Played",
                   "Goals", "Assists", "Goals per Game", "Assists per Game", "Contributions per Game (Goals + Assists)"]

    ###### Win % #######
    wdl_table_final = all_final[["Win Draw Loss", "Player", "Goals"]].groupby(["Player", "Win Draw Loss"]).count().T
    played_final = all_final[["Dates", "Player"]].groupby(["Player"]).count().T

    ronaldo_table_final.append("{}%".format(round(wdl_table_final["Cristiano Ronaldo"]["W"].tolist()[0] / played_final["Cristiano Ronaldo"].tolist()[0] * 100, 2)))
    messi_table_final.append("{}%".format(round(wdl_table_final["Lionel Messi"]["W"].tolist()[0] / played_final["Lionel Messi"].tolist()[0] * 100, 2)))

    ###### Loss % #######
    ronaldo_table_final.append("{}%".format(round(wdl_table_final["Cristiano Ronaldo"]["L"].tolist()[0] / played_final["Cristiano Ronaldo"].tolist()[0] * 100, 2)))
    messi_table_final.append("{}%".format(round(wdl_table_final["Lionel Messi"]["L"].tolist()[0] / played_final["Lionel Messi"].tolist()[0] * 100, 2)))

    ###### WDL #######
    ronaldo_table_final.append(wdl_table_final["Cristiano Ronaldo"]["W"].tolist()[0])
    ronaldo_table_final.append(wdl_table_final["Cristiano Ronaldo"]["L"].tolist()[0])
    messi_table_final.append(wdl_table_final["Lionel Messi"]["W"].tolist()[0])
    messi_table_final.append(wdl_table_final["Lionel Messi"]["L"].tolist()[0])

    ###### Played #######
    ronaldo_table_final.append(played_final["Cristiano Ronaldo"].tolist()[0])
    messi_table_final.append(played_final["Lionel Messi"].tolist()[0])

    ###### Goals #######
    goals_final = all_final[["Goals", "Player"]].groupby(["Player"]).sum().T
    ronaldo_table_final.append(goals_final["Cristiano Ronaldo"].tolist()[0])
    messi_table_final.append(goals_final["Lionel Messi"].tolist()[0])

    ###### Assists #######
    assists_final = all_final[["Assists", "Player"]].groupby(["Player"]).sum().T
    ronaldo_table_final.append(assists_final["Cristiano Ronaldo"].tolist()[0])
    messi_table_final.append(assists_final["Lionel Messi"].tolist()[0])

    ###### Goals per Game #######
    ronaldo_table_final.append(round((goals_final["Cristiano Ronaldo"].tolist()[0]) / played_final["Cristiano Ronaldo"].tolist()[0], 2))
    messi_table_final.append(round((goals_final["Lionel Messi"].tolist()[0]) / played_final["Lionel Messi"].tolist()[0], 2))

    ###### Assists per Game #######
    ronaldo_table_final.append(round((assists_final["Cristiano Ronaldo"].tolist()[0]) / played_final["Cristiano Ronaldo"].tolist()[0], 2))
    messi_table_final.append(round((assists_final["Lionel Messi"].tolist()[0]) / played_final["Lionel Messi"].tolist()[0], 2))

    ###### Contribution Per Game #######
    ronaldo_table_final.append(round((goals_final["Cristiano Ronaldo"].tolist()[0] + assists_final["Cristiano Ronaldo"].tolist()[0]) / played_final["Cristiano Ronaldo"].tolist()[0], 2))
    messi_table_final.append(round((goals_final["Lionel Messi"].tolist()[0] + assists_final["Lionel Messi"].tolist()[0]) / played_final["Lionel Messi"].tolist()[0], 2))

    traces = []

    traces.append(go.Table(
                header=dict(values=list(["", "Lionel Messi", "Cristiano Ronaldo"]),
                            fill_color='#222831',
                            line_color='white',
                            font=dict(color='white', size=13),
                            align='center'),
                cells=dict(values=[value_names_final, messi_table_final, ronaldo_table_final]))

        )
    return {"data": traces, "layout": go.Layout(title={'text': "Player Performance in {}".format(specific_comp),
                               'x':0.5},
                        height = 450,
                        template= "plotly_dark",
                        paper_bgcolor = '#686868')}
