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

app.layout = html.Div([
    html.H4('Interactive color selection with simple Dash example'),
    html.P("Select color:"),
    dcc.Dropdown(
        id="dropdown",
        options=['Gold', 'MediumTurquoise', 'LightGreen'],
        value='Gold',
        clearable=False,
    ),
    dcc.Graph(id="graph"),
    dcc.Graph(id="graph2"),
])

@app.callback(
    Output("graph", "figure"), 
    Input("dropdown", "value"))
def buggaBugga(color):
    fig = go.Figure(
        data=go.Bar(y=numLanguages, x=names, # replace with your own data source
                    marker_color=color))
    return fig

@app.callback(
    Output("graph2", "figure"), 
    Input("dropdown", "value"))
def buggaBugga(color):
    fig = go.Figure(
        data=go.Box(y=ages, x=names, # replace with your own data source
                    marker_color=color))
    return fig


app.run_server(debug=True)