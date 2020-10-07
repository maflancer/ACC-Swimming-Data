import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server

male_data = pd.read_csv('./data/swimmers_male_times.csv')
female_data = pd.read_csv('./data/swimmers_female_times.csv')
male_ppe_data = pd.read_csv('./data/swimmers_male_data.csv')
female_ppe_data = pd.read_csv('./data/swimmers_female_data.csv')
acc_image_src = 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Atlantic_Coast_Conference_logo.svg/1200px' \
                '-Atlantic_Coast_Conference_logo.svg.png '

teams = male_data['Team'].unique()
years = male_data['Year'].unique()

# ---------------------HELPER FUNCTIONS------------------------------

def convertTime(displayTime):
    if ':' in displayTime:
        timeArray = displayTime.split(':')
        seconds = float(timeArray[0]) * 60
        seconds += float(timeArray[1])

        return seconds
    elif displayTime.isalpha():
        print('')  # do nothing
    else:
        return float(displayTime)

def addTimes(df):
    allPrelimTimes = []
    allPrelimYears = []
    allFinalTimes = []
    allFinalYears = []

    for index, row in df.iterrows():
        time = convertTime(row['Time'])

        if row['Event_Type'] == 'Prelims' and isinstance(time, float):
            allPrelimTimes.append(time)
            allPrelimYears.append(row['Year'])
        if row['Event_Type'] == 'Finals' and isinstance(time, float):
            allFinalTimes.append(time)
            allFinalYears.append(row['Year'])

    return allPrelimTimes, allPrelimYears, allFinalTimes, allFinalYears

# ---------------------APP LAYOUT----------------------------------------------

app.layout = html.Div([
    dcc.Tabs(id='swimming-tabs', value='swimmer-improvement', children=[
        dcc.Tab(label='Swimmer Improvement Graph', value='swimmer-improvement'),
        dcc.Tab(label='Swimmer Points Per Event (PPE) Graph', value='ppe-graph'),
    ]),
    html.Div(id='swimming-tabs-content')
])


# ---------------------APP CALLBACKS---------------------------------------------

@app.callback(Output('swimming-tabs-content', 'children'),
              [Input('swimming-tabs', 'value')])
def render_content(tab):
    if tab == 'swimmer-improvement':
        return (
            html.Div([

                html.Div([html.Img(src=acc_image_src,
                                   style={'height': 'auto', 'width': '200px', 'display': 'block', 'margin': 'auto'})],
                         style={'padding-bottom': '20px', 'padding-top': '20px'}),

                html.Div([
                    html.H6(children='Gender'),
                    dcc.Dropdown(
                        id='gender-dropdown',
                        options=[{'label': 'Male', 'value': 'Male'}, {'label': 'Female', 'value': 'Female'}],
                        placeholder = 'Select a gender'
                    )
                ],
                    style={'width': '13%', 'float': 'left'}),

                html.Div([
                    html.H6(children='Team'),
                    dcc.Dropdown(
                        id='team-dropdown',
                        options=[{'label': i, 'value': i} for i in teams],
                        value='Team',
                        placeholder = 'Select a team'
                    )
                ],
                    style={'width': '16%', 'float': 'left', 'margin-left': '30px'}),

                html.Div([
                    html.H6(children = 'Year'),
                    dcc.Dropdown(
                        id = 'year-dropdown',
                        options = [{'label' : i, 'value' : i} for i in years],
                        value = 'Year',
                        multi = True,
                        placeholder = 'Filter by year (optional)'
                    )
                ],
                style = {'width' : '13%', 'float' : 'left', 'margin-left' : '30px'}),

                html.Div([
                    html.H6(children='Swimmer'),
                    dcc.Dropdown(id='player-dropdown', placeholder = 'Select a swimmer')
                ],
                    style={'width': '13%', 'float': 'left', 'margin-left': '30px'}),

                html.Div([
                    html.H6(children='Event'),
                    dcc.Dropdown(id='event-dropdown', placeholder = 'Select an event')
                ],
                    style={'width': '13%', 'float': 'left', 'margin-left': '30px'}),

                html.Div([
                    dcc.Checklist(
                        id='average-team-checklist',
                        options=[{'label': 'Team Average', 'value': 'Team Average'}]
                    )
                ],
                    style={'float': 'left', 'padding-top': '50px', 'margin-left': '10px'}),

                html.Div([
                    dcc.Checklist(
                        id='average-acc-checklist',
                        options=[{'label': 'ACC Average', 'value': 'ACC Average'}]
                    )
                ],
                    style={'float': 'left', 'padding-top': '50px', 'margin-left': '10px'}),

                html.Div([
                    dcc.Graph(id='improvement-graph')
                ],
                    style={'padding-top': '100px'})
            ])
        )
    elif tab == 'ppe-graph':
        return (
            html.Div([
                html.Div([html.Img(src=acc_image_src,
                                   style={'height': 'auto', 'width': '200px', 'display': 'block', 'margin': 'auto'})],
                         style={'padding-bottom': '20px', 'padding-top': '20px'}),

                html.Div([
                    html.H6(children='Gender'),
                    dcc.Dropdown(
                        id='ppe-gender-dropdown',
                        options=[{'label': 'Male', 'value': 'Male'}, {'label': 'Female', 'value': 'Female'}],
                        placeholder = 'Select a gender'
                    )
                ],
                    style={'width': '16%', 'float': 'left', 'margin-left': '60px'}),

                html.Div([
                    html.H6(children='Team'),
                    dcc.Dropdown(
                        id='ppe-team-dropdown',
                        options=[{'label': i, 'value': i} for i in teams],
                        value='Team',
                        placeholder = 'Select a team'
                    )
                ],
                    style={'width': '16%', 'float': 'left', 'margin-left': '60px'}),

                html.Div([
                    html.H6(children = 'Year'),
                    dcc.Dropdown(
                        id = 'ppe-year-dropdown',
                        options = [{'label' : i, 'value' : i} for i in years],
                        value = 'Year',
                        multi = True,
                        placeholder = 'Filter by year (optional)'
                    )
                ],
                style = {'width' : '16%', 'float' : 'left', 'margin-left' : '60px'}),

                html.Div([
                    html.H6(children='Swimmer'),
                    dcc.Dropdown(id='ppe-player-dropdown', placeholder = 'Select a swimmer')
                ],
                    style={'width': '16%', 'float': 'left', 'margin-left': '60px'}),

                html.Div([
                    dcc.Checklist(
                        id='ppe-average-team-checklist',
                        options=[{'label': 'Team Average', 'value': 'Team Average'}]
                    )
                ],
                    style={'float': 'left', 'padding-top': '50px', 'margin-left': '30px'}),

                html.Div([
                    dcc.Checklist(
                        id='ppe-average-acc-checklist',
                        options=[{'label': 'ACC Average', 'value': 'ACC Average'}]
                    )
                ],
                    style={'float': 'left', 'padding-top': '50px', 'margin-left': '30px'}),

                html.Div([
                    dcc.Graph(id='ppe-graph')
                ],
                    style={'padding-top': '100px'})
            ])
        )


# -----------------SWIMMER IMPROVEMENT GRAPH CALLBACKS----------------------------------

@app.callback(
    Output('player-dropdown', 'options'),
    [Input('team-dropdown', 'value'),
     Input('gender-dropdown', 'value'),
     Input('year-dropdown', 'value')])
def set_player_options(selected_team, gender, selected_years):
    data = male_data

    if gender == 'Female':
        data = female_data

    players = []
    swimmerIds = []

    if(isinstance(selected_years, str) or len(selected_years) == 0):
        for index, row in data.iterrows():
            if row['Team'] == selected_team and not row['Swimmer_ID'] in swimmerIds:
                players.append({'label' : row['Name'], 'value' : row['Swimmer_ID']})
                swimmerIds.append(row['Swimmer_ID'])
    else:
        for index, row in data.iterrows():
            if row['Team'] == selected_team and row['Year'] in selected_years and not row['Swimmer_ID'] in swimmerIds:
                players.append({'label' : row['Name'], 'value' : row['Swimmer_ID']})
                swimmerIds.append(row['Swimmer_ID'])

    return players


@app.callback(
    Output('player-dropdown', 'value'),
    [Input('player-dropdown', 'options')])
def set_player_value(available_options):
    if len(available_options) == 0:
        return 'Name'
    else:
        return available_options[0]['value']


@app.callback(
    Output('event-dropdown', 'options'),
    [Input('player-dropdown', 'value'),
     Input('gender-dropdown', 'value')])
def set_event_options(selected_player, gender):
    data = male_data

    if gender == 'Female':
        data = female_data

    events = []
    event_names = []
    for index, row in data.iterrows():
        if row['Swimmer_ID'] == selected_player and not row['Event'] in event_names and not row['Event_Type'] == 'Timed Finals':
            events.append({'label': row['Event'], 'value': row['Event']})
            event_names.append(row['Event'])

    return events


@app.callback(
    Output('event-dropdown', 'value'),
    [Input('event-dropdown', 'options')])
def set_event_value(available_options):
    if len(available_options) == 0:
        return 'Event'
    else:
        return available_options[0]['value']


@app.callback(
    Output('improvement-graph', 'figure'),
    [Input('gender-dropdown', 'value'),
     Input('team-dropdown', 'value'),
     Input('player-dropdown', 'value'),
     Input('event-dropdown', 'value'),
     Input('average-team-checklist', 'value'),
     Input('average-acc-checklist', 'value')])
def update_graph(gender, team, Swimmer_ID, event, team_value, acc_value):
    data = male_data

    if (gender == 'Female'):
        data = female_data

    diveCheck = False

    if (event[-6:] == 'Diving' or event[-6:] == 'dives)'):  # if diving event
        diveCheck = True

    newData = data[data['Swimmer_ID'] == Swimmer_ID]
    newData = newData[newData['Event'] == event]

    playerPrelimTimes, playerPrelimYears, playerFinalTimes, playerFinalYears = addTimes(newData)

    if (team_value):
        if (len(playerPrelimYears) > 0):
            startYear = playerPrelimYears[0]
            endYear = playerPrelimYears[len(playerPrelimYears) - 1]
        else:
            startYear = 0
            endYear = 0

        teamPrelimTimes = []
        teamPrelimYears = []
        teamFinalTimes = []
        teamFinalYears = []

        teamData = data[data['Event'] == event]
        teamData = teamData[teamData['Team'] == team]

        for i in range(startYear, endYear + 1):
            newTeamData = teamData[teamData['Year'] == i]
            tempPrelimTimes, tempPrelimYears, tempFinalTimes, tempFinalYears = addTimes(newTeamData)

            if (len(tempPrelimYears) > 0):
                teamPrelimTimes.append(np.mean(tempPrelimTimes))
                teamPrelimYears.append(tempPrelimYears[0])
            if (len(tempFinalTimes) > 0):
                teamFinalTimes.append(np.mean(tempFinalTimes))
                teamFinalYears.append(tempFinalYears[0])

    if (acc_value):
        if (len(playerPrelimYears) > 0):
            startYear = playerPrelimYears[0]
            endYear = playerPrelimYears[len(playerPrelimYears) - 1]
        else:
            startYear = 0
            endYear = 0

        accPrelimTimes = []
        accPrelimYears = []
        accFinalTimes = []
        accFinalYears = []

        accData = data[data['Event'] == event]

        for i in range(startYear, endYear + 1):
            newAccData = accData[accData['Year'] == i]
            tempPrelimTimes, tempPrelimYears, tempFinalTimes, tempFinalYears = addTimes(newAccData)

            if (len(tempPrelimYears) > 0):
                accPrelimTimes.append(np.mean(tempPrelimTimes))
                accPrelimYears.append(tempPrelimYears[0])
            if (len(tempFinalTimes) > 0):
                accFinalTimes.append(np.mean(tempFinalTimes))
                accFinalYears.append(tempFinalYears[0])

    scatters = [go.Scatter(name='Prelims', x=playerPrelimYears, y=playerPrelimTimes, marker=dict(color='Blue')),
                go.Scatter(name='Finals', x=playerFinalYears, y=playerFinalTimes, marker=dict(color='skyblue'))]

    if (team_value):
        scatters.append(go.Scatter(name='Team Average - Prelims', x=teamPrelimYears, y=teamPrelimTimes, opacity=.7,
                                   marker=dict(color='Red')))
        scatters.append(go.Scatter(name='Team Average - Finals', x=teamFinalYears, y=teamFinalTimes, opacity=.7,
                                   marker=dict(color='orangered')))

    if (acc_value):
        scatters.append(go.Scatter(name='ACC Average - Prelims', x=accPrelimYears, y=accPrelimTimes, opacity=.7,
                                   marker=dict(color='Orange')))
        scatters.append(go.Scatter(name='ACC Average - Finals', x=accFinalYears, y=accFinalTimes, opacity=.7,
                                   marker=dict(color='brown')))

    fig = go.Figure(data=scatters)

    fig.update_layout(xaxis_title='Year', yaxis_title='Seconds')

    if (len(playerPrelimYears) > 0):
        fig.update_layout(barmode='group', xaxis=dict(tickmode='array', tickvals=playerPrelimYears), xaxis_title='Year',
                          yaxis_title='Seconds')

    if (diveCheck):
        fig.update_layout(yaxis_title='Points')

    return fig


# ----------------------------------SWIMMER PPE GRAPH CALLBACKS------------------------------------------------

@app.callback(
    Output('ppe-player-dropdown', 'options'),
    [Input('ppe-team-dropdown', 'value'),
     Input('ppe-gender-dropdown', 'value'),
     Input('ppe-year-dropdown', 'value')])
def ppe_set_player_options(selected_team, gender, selected_years):
    data = male_ppe_data

    if (gender == 'Female'):
        data = female_ppe_data

    players = []
    swimmerIds = []

    if(isinstance(selected_years, str) or len(selected_years) == 0):
        for index, row in data.iterrows():
            if row['Team'] == selected_team and not row['Swimmer_ID'] in swimmerIds:
                players.append({'label' : row['Name'], 'value' : row['Swimmer_ID']})
                swimmerIds.append(row['Swimmer_ID'])
    else:
        for index, row in data.iterrows():
            yearCheck = False
            start = row['Starting season'] + 1997        #this gets the correct year from the season id where season id 17 = year 2014
            yearValues = list(range(start, start + 4))   #creates list of years from start year to start year + 4 so it would be [2014 - 2018)
            for year in yearValues:
                if year in selected_years:
                    yearCheck = True

            if row['Team'] == selected_team and yearCheck is True and not row['Swimmer_ID'] in swimmerIds:
                players.append({'label' : row['Name'], 'value' : row['Swimmer_ID']})
                swimmerIds.append(row['Swimmer_ID'])


    return players


@app.callback(
    Output('ppe-player-dropdown', 'value'),
    [Input('ppe-player-dropdown', 'options')])
def ppe_set_player_value(available_options):
    if (len(available_options) == 0):
        return 'Name'
    else:
        return available_options[0]['value']


@app.callback(
    Output('ppe-graph', 'figure'),
    [Input('ppe-gender-dropdown', 'value'),
     Input('ppe-team-dropdown', 'value'),
     Input('ppe-player-dropdown', 'value'),
     Input('ppe-average-team-checklist', 'value'),
     Input('ppe-average-acc-checklist', 'value')])
def ppe_update_graph(gender, team, Swimmer_ID, team_value, acc_value):
    data = male_ppe_data

    if (gender == 'Female'):
        data = female_ppe_data

    newData = data[data['Swimmer_ID'] == Swimmer_ID]

    ppe = []
    grades = []

    for index, row in newData.iterrows():
        if ((row['Events-FR']) > 0):
            ppe.append(row['Freshman_PPE'])
            grades.append('FR')
        elif ((row['Events-SO']) > 0 or (row['Events-JR']) > 0 or (row['Events-SR']) > 0):
            ppe.append(row['Freshman_PPE'])
            grades.append('FR')
        if ((row['Events-SO']) > 0):
            ppe.append(row['Sophomore_PPE'])
            grades.append('SO')
        elif ((row['Events-JR']) > 0 or (row['Events-SR']) > 0):
            ppe.append(row['Sophomore_PPE'])
            grades.append('SO')
        if ((row['Events-JR']) > 0):
            ppe.append(row['Junior_PPE'])
            grades.append('JR')
        elif ((row['Events-SR']) > 0):
            ppe.append(row['Junior_PPE'])
            grades.append('JR')
        if ((row['Events-SR']) > 0):
            ppe.append(row['Senior_PPE'])
            grades.append('SR')

    if (team_value):
        teamData = data[data['Team'] == team]

        ppe_FR = []
        ppe_SO = []
        ppe_JR = []
        ppe_SR = []

        for index, row in teamData.iterrows():
            if ((row['Events-FR']) > 0 and (row['Events-SO']) > 0 and (row['Events-JR']) > 0 and (
            row['Events-SR']) > 0):
                ppe_FR.append(row['Freshman_PPE'])
                ppe_SO.append(row['Sophomore_PPE'])
                ppe_JR.append(row['Junior_PPE'])
                ppe_SR.append(row['Senior_PPE'])

        team_ppe = [np.mean(ppe_FR), np.mean(ppe_SO), np.mean(ppe_JR), np.mean(ppe_SR)]

    if (acc_value):
        acc_ppe_FR = []
        acc_ppe_SO = []
        acc_ppe_JR = []
        acc_ppe_SR = []

        for index, row in data.iterrows():
            if ((row['Events-FR']) > 0 and (row['Events-SO']) > 0 and (row['Events-JR']) > 0 and (
            row['Events-SR']) > 0):
                acc_ppe_FR.append(row['Freshman_PPE'])
                acc_ppe_SO.append(row['Sophomore_PPE'])
                acc_ppe_JR.append(row['Junior_PPE'])
                acc_ppe_SR.append(row['Senior_PPE'])

        acc_team_ppe = [np.mean(acc_ppe_FR), np.mean(acc_ppe_SO), np.mean(acc_ppe_JR), np.mean(acc_ppe_SR)]

    scatters = [go.Scatter(name='Swimmer_PPE', x=grades, y=ppe, marker=dict(color='Blue'))]

    if (team_value):
        scatters.append(
            go.Scatter(name='Team_Average_PPE', x=['FR', 'SO', 'JR', 'SR'], y=team_ppe, marker=dict(color='Red')))

    if (acc_value):
        scatters.append(
            go.Scatter(name='ACC_Average_PPE', x=['FR', 'SO', 'JR', 'SR'], y=acc_team_ppe, marker=dict(color='Green')))

    fig = go.Figure(data=scatters)

    fig.update_layout(xaxis_title='Grade', yaxis_title='Points Per Event (PPE)')
    fig.update_layout(showlegend=True)

    return fig


# ---------MAIN-------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
