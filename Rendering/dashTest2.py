from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np
import json

app = Dash(__name__)

# with open('path_to_file/person.json', 'r') as f:
#   data = json.load(f) # as dictionary
classroom = '''{"classroom": [
    {"name": "Bob", "age": 12, "languages": ["English", "French"]},
    {"name": "John", "age": 13, "languages": ["English"]},
    {"name": "Boby", "age": 12, "languages": ["English", "French", "Spanish"]}
    ]}'''
classroom_dict = json.loads(classroom)

print(classroom_dict)
names = np.empty(len(classroom_dict['classroom']), dtype='object')
ages = np.zeros(len(classroom_dict['classroom']))
languages = np.empty(len(classroom_dict['classroom']), dtype='object')
numLanguages = np.zeros(languages.size)
i = 0
for person in classroom_dict['classroom']:
    names[i] = person['name']
    ages[i] = person['age']
    languages[i] = person['languages']
    numLanguages[i] = len(languages[i])
    print(names[i] + ':', ages[i], languages[i])
    i += 1


datExample = '''{[
    {"userID": "1", "level1-Time": 10, "level2-Time": 20, "level3-Time": 40},
    {"userID": "2", "level1-Time": 8, "level2-Time": 17, "level3-Time": 42},
]}'''

size = 100
numLevels = 3

levels = np.append(np.append(np.zeros(size), np.ones(size)), np.ones(size) + 1)
levelsNames = ["Level 1", "Level 2", "Level 3"]

level1Time = np.random.uniform(low=5, high=15, size=(size,))
level2Time = np.random.uniform(low=10, high=25, size=(size,))
level3Time = np.random.uniform(low=10, high=55, size=(size,))
times = np.append(np.append(level1Time, level2Time), level3Time)

level1Tries = np.random.randint(low=15, high=30, size=(size,))
level2Tries = np.random.randint(low=3, high=25, size=(size,))
level3Tries = np.random.randint(low=40, high=70, size=(size,))
tries = np.append(np.append(level1Tries, level2Tries), level3Tries)

level1Help = np.sum(np.random.choice(a=[True, False], size=(size,), p=[0.2, 0.8]))
level2Help = np.sum(np.random.choice(a=[True, False], size=(size,), p=[0.5, 0.5]))
level3Help = np.sum(np.random.choice(a=[True, False], size=(size,), p=[0.7, 0.3]))

helps = [level1Help, level2Help, level3Help]
notHelps = [size - level1Help, size - level2Help, size - level3Help]

level1Optim = np.sum(np.random.choice(a=[True, False], size=(size,), p=[0.8, 0.2]))
level2Optim = np.sum(np.random.choice(a=[True, False], size=(size,), p=[0.5, 0.5]))
level3Optim = np.sum(np.random.choice(a=[True, False], size=(size,), p=[0.3, 0.7]))

optim = [level1Optim, level2Optim, level3Optim]
notOptim = [size - level1Optim, size - level2Optim, size - level3Optim]

app.layout = html.Div([
    html.H4('Interactive color selection with simple Dash example'),
    html.P("Select color:"),
    dcc.Dropdown(
        id="dropdown",
        options=['Gold', 'MediumTurquoise', 'LightGreen', 'DarkGrey'],
        value='Gold',
        clearable=False,
    ),
    #dcc.Graph(id="graph"),
    #dcc.Graph(id="graph2"),
    #dcc.Graph(id="graphTime1"),
    dcc.Graph(id="graphTime", style={'height':'1000px'}),
    dcc.Graph(id="graphTries", style={'height':'1000px'}),
    dcc.Graph(id="graphHelp", style={'width': '90vh', 'height':'800px'}),
    dcc.Graph(id="graphOptim", style={'width': '90vh', 'height':'800px'}),
    dcc.Graph(id="graphTest", style={'height':'1000px'}),

])

# @app.callback(
#     Output("graph", "figure"), 
#     Input("dropdown", "value"))
# def buggaBugga(color):
#     fig = go.Figure(
#         data=go.Bar(y=numLanguages, x=names, # replace with your own data source
#                     marker_color=color))
#     return fig

# @app.callback(
#     Output("graph2", "figure"), 
#     Input("dropdown", "value"))
# def buggaBugga(color):
#     fig = go.Figure(
#         data=go.Box(y=ages, x=names, # replace with your own data source
#                     marker_color=color))
#     return fig

# @app.callback(
#     Output("graphTime1", "figure"), 
#     Input("dropdown", "value"))
# def buggaBugga(color):
#     fig = go.Figure(
#         data=go.Scatter(y=times, x=levels, # replace with your own data source
                    
#                     mode='markers',
#                     marker_color=color,
#                     name='Time values'))
#     fig.add_trace(go.Scatter(x=[0,1,2], y=[np.average(level1Time),np.average(level2Time),np.average(level3Time)], 
#                     name='Average time'))
#     return fig

@app.callback(
    Output("graphTime", "figure"), 
    Input("dropdown", "value"))
def buggaBugga(color):
    fig = go.Figure(
        data=go.Box(y=times, x=levels, # replace with your own data source
                    boxpoints='all',
                    pointpos=0,
                    fillcolor='rgba(0,0,0,0.1)',
                    #marker_color=color,
                    name='Time values'))
    fig.add_trace(go.Scatter(x=[0,1,2], y=[np.average(level1Time),np.average(level2Time),np.average(level3Time)], 
                    name='Average time'))
    fig.update_xaxes(
                    ticktext= levelsNames,
                    tickvals=[0,1,2])
    return fig

@app.callback(
    Output("graphTries", "figure"), 
    Input("dropdown", "value"))
def buggaBugga(color):
    fig = go.Figure(
        data=go.Box(y=tries, x=levels, # replace with your own data source
                    boxpoints='all',
                    pointpos=0,
                    fillcolor='rgba(0,0,0,0.1)',
                    #marker_color=color,
                    name='Tries values'))
    fig.add_trace(go.Scatter(x=[0,1,2], y=[np.average(level1Tries),np.average(level2Tries),np.average(level3Tries)], 
                    name='Average Tries'))
    fig.update_xaxes(
                    ticktext= levelsNames,
                    tickvals=[0,1,2])
    return fig

@app.callback(
    Output("graphHelp", "figure"), 
    Input("dropdown", "value"))
def buggaBugga(color):
    fig = go.Figure(data=[
            go.Bar(y=helps, x=levelsNames, # replace with your own data source
            name='Helped'),
            go.Bar(y=notHelps, x=levelsNames, 
            name='Not helped')])
    fig.update_layout(barmode='stack')
    return fig

@app.callback(
    Output("graphOptim", "figure"), 
    Input("dropdown", "value"))
def buggaBugga(color):
    fig = go.Figure(data=[
            go.Bar(y=optim, x=levelsNames, # replace with your own data source
            name='Optimal solution'),
            go.Bar(y=notOptim, x=levelsNames, 
            name='Not optimal')])
    fig.update_layout(barmode='stack')
    return fig

@app.callback(
    Output("graphTest", "figure"), 
    Input("dropdown", "value"))
def buggaBugga(color):
    fig = go.Figure()
    fig.add_trace(go.Box(y=tries, x=levels, # replace with your own data source
                    boxpoints='all',
                    pointpos=0,
                    fillcolor='rgba(0,0,0,0.1)',
                    name='Con Experiencia'))
    fig.add_trace(go.Box(y=times, x=levels, # replace with your own data source
                    boxpoints='all',
                    pointpos=0,
                    fillcolor='rgba(0,0,0,0.1)',
                    name='Sin Experiencia'))
    fig.update_xaxes(
                    ticktext= levelsNames,
                    tickvals=[0,1,2])

    fig.update_layout(
            yaxis_title='Duracion de los intentos',
            boxmode='group' # group together boxes of the different traces for each value of x
    )
    return fig

app.run_server(debug=True)