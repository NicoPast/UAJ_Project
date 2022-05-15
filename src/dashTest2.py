from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np
import json
from processData import getProbadores,agruparProbadores,separarProbadores

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

Probadores=getProbadores()
NivelesGeneral=agruparProbadores(Probadores)
levelsNames = NivelesGeneral.keys()

size = len(Probadores)
numLevels = len(levelsNames)


vals = [i for i in range(numLevels)]

factor = 1/(numLevels*2)
startPoint = factor * numLevels/2

helps = []
helpsNoExp = []
helpsExp = []
notHelps = []
notHelpsNoExp = []
notHelpsExp = []
optim = []
optimNoExp = []
optimExp = []
notOptim = []
notOptimNoExp = []
notOptimExp = []

levels = np.empty(0)
times = list()
timesExp = np.empty(0)
timesNoExp = np.empty(0)
tries = np.empty(0)
triesExp = np.empty(0)
triesNoExp = np.empty(0)
codeLength = np.empty(0)
codeLengthExp = np.empty(0)
codeLengthNoExp = np.empty(0)

for i in range(numLevels):

    levels = np.append(levels,np.zeros(size) + i)
    times.append(np.array(list(NivelesGeneral.values())[i]['playTime']))
    timesExp = np.append(timesExp, np.random.uniform(
        low=5 + i, high=30 + i, size=(size,)))
    timesNoExp = np.append(timesNoExp, np.random.uniform(
        low=10 + 5 * i, high=30 + 5 * i, size=(size,)))

    tries = np.append(tries,np.array(list(NivelesGeneral.values())[i]['tries']))
    triesExp = np.append(triesExp, np.random.randint(
        low=5 + i, high=25 + i, size=(size,)))
    triesNoExp = np.append(triesNoExp, np.random.randint(
        low=8 + 5 * i, high=30 + 5 * i, size=(size,)))

    codeLength = np.append(codeLength,np.array(list(NivelesGeneral.values())[i]['codeLength']))
    codeLengthExp = np.append(codeLengthExp, np.random.randint(
        low=7 + i, high=25 + i, size=(size,)))
    codeLengthNoExp = np.append(codeLengthNoExp, np.random.randint(
        low=10 + 5 * i, high=30 + 5 * i, size=(size,)))

    helps.append(np.sum(np.random.choice(
        a=[True, False], size=(size,), p=[startPoint + factor * i, 1 - (startPoint + factor * i)]
    )))
    notHelps.append(size - helps[i])

    helpsNoExp.append(np.sum(np.random.choice(
        a=[True, False], size=(size,), p=[startPoint + factor * i, 1 - (startPoint + factor * i)]
    )))
    notHelpsNoExp.append(size - helpsNoExp[i])

    helpsExp.append(np.sum(np.random.choice(
        a=[True, False], size=(size,), p=[startPoint + factor * i, 1 - (startPoint + factor * i)]
    )))
    notHelpsExp.append(size - helpsExp[i])

    optim.append(np.sum(np.array(list(NivelesGeneral.values())[i]['codeOptimo'])))
    notOptim.append(size - optim[i])

    optimNoExp.append(np.sum(np.random.choice(
        a=[True, False], size=(size,), p=[1 - (startPoint + factor * i), startPoint + factor * i]
    )))
    notOptimNoExp.append(size - optimNoExp[i])

    optimExp.append(np.sum(np.random.choice(
        a=[True, False], size=(size,), p=[1 - (startPoint + factor * i), startPoint + factor * i]
    )))
    notOptimExp.append(size - optimExp[i]) 


app.layout = html.Div([

    html.H1('Titulo de la investigación', style={'font-size': '70px'}),
    html.P('En este proyecto, se tiene como objetivo realizar un análisis de usabilidad sobre el TFG de uno de los integrantes del grupo. Dicho TFG consiste en el desarrollo de un juego serio cuyo objetivo es la enseñanza de conceptos de Computational Thinking y nuestro objetivo es realizar pruebas sobre usuarios que nunca han estado en contacto con el proyecto'),
    html.H1('Curva de aprendizaje', style={'font-size': '50px'}),
    dcc.Graph(id="graphTime", style={'height': '800px'}),
    dcc.Graph(id="graphTries", style={'height': '800px'}),
    dcc.Graph(id="graphCodeLength", style={'height': '800px'}),
    dcc.Graph(id="graphHelp", style={'height': '800px'}),
    dcc.Graph(id="graphOptim", style={'height': '800px'}),
    html.H1('Comparativa de experiencia previa', style={'font-size': '50px'}),
    dcc.Graph(id="graphTimeCompare", style={'height': '800px'}),
    dcc.Graph(id="graphTriesCompare", style={'height': '800px'}),
    dcc.Graph(id="graphCodeLengthCompare", style={'height': '800px'}),
    dcc.Graph(id="graphHelpCompare", style={'height': '800px'}),
    dcc.Graph(id="graphOptimCompare", style={'height': '800px'}),

    dcc.Dropdown(
        id="dropdown",
        options=['Gold', 'MediumTurquoise', 'LightGreen', 'DarkGrey'],
        value='Gold',
        clearable=False,
        style={'display': 'none'}
    )

], style={'width': '100%', 'textAlign': 'center', 'display': 'inline-block'})


@app.callback(
    Output("graphTime", "figure"),
    Input("dropdown", "value"))
def buggaBugga(color):
    fig = go.Figure(
        data=go.Box(y=times, x=levels,  # replace with your own data source
                    boxpoints='all',
                    pointpos=0,
                    fillcolor='rgba(0,0,0,0.1)',
                    # marker_color=color,
                    name='Time values'),
        layout=go.Layout(
            title=go.layout.Title(
                text='Tiempo dedicado'
            )
        ))

    fig.add_trace(go.Scatter(x=vals, y=[np.average(times[i]) for i in range(numLevels)], name='Average time'))

    fig.update_xaxes(
        ticktext=levelsNames,
        tickvals=vals)
    fig.update_yaxes(title="Tiempo")
    return fig


@app.callback(
    Output("graphTries", "figure"),
    Input("dropdown", "value"))
def buggaBugga(color):
    fig = go.Figure(
        data=go.Box(y=tries, x=levels,  # replace with your own data source
                    boxpoints='all',
                    pointpos=0,
                    fillcolor='rgba(0,0,0,0.1)',
                    # marker_color=color,
                    name='Tries values'),
        layout=go.Layout(
            title=go.layout.Title(
                text='Intentos por nivel'
            )
        ))
    fig.add_trace(go.Scatter(x=vals, y=[np.average(tries[size*i:size*(i+1)]) for i in range(numLevels)],
                             name='Average Tries'))
    fig.update_xaxes(
        ticktext=levelsNames,
        tickvals=vals)
    fig.update_yaxes(title="Intentos")
    return fig


@app.callback(
    Output("graphCodeLength", "figure"),
    Input("dropdown", "value"))
def buggaBugga(color):
    fig = go.Figure(
        data=go.Box(y=codeLength, x=levels,  # replace with your own data source
                    boxpoints='all',
                    pointpos=0,
                    fillcolor='rgba(0,0,0,0.1)',
                    # marker_color=color,
                    name='Tries values'),
        layout=go.Layout(
            title=go.layout.Title(
                text='Longitud del código'
            )
        ))
    fig.add_trace(go.Scatter(x=vals, y=[np.average(codeLength[size*i:size*(i+1)]) for i in range(numLevels)],
                             name='Average Tries'))
    fig.update_xaxes(
        ticktext=levelsNames,
        tickvals=vals)

    fig.update_yaxes(title="Longitud")
    return fig


@app.callback(
    Output("graphHelp", "figure"),
    Input("dropdown", "value"))
def buggaBugga(color):
    fig = go.Figure(data=[
        go.Bar(y=helps, x=levelsNames,  # replace with your own data source
               name='Helped'),
        go.Bar(y=notHelps, x=levelsNames,
               name='Not helped')],
        layout=go.Layout(
            title=go.layout.Title(
                text='Numero de Ayudas utilizadas'
            )
    ))
    fig.update_layout(barmode='stack')
    fig.update_yaxes(title="Usuarios")
    return fig


@app.callback(
    Output("graphOptim", "figure"),
    Input("dropdown", "value"))
def buggaBugga(color):
    fig = go.Figure(data=[
        go.Bar(y=optim, x=levelsNames,  # replace with your own data source
               name='Optimal solution'),
        go.Bar(y=notOptim, x=levelsNames,
               name='Not optimal')],
        layout=go.Layout(
            title=go.layout.Title(
                text='Soluciones óptimas'
            )
    ))
    fig.update_layout(barmode='stack')
    fig.update_yaxes(title="Usuarios")
    return fig


@app.callback(
    Output("graphTimeCompare", "figure"),
    Input("dropdown", "value"))
def buggaBugga(color):
    fig = go.Figure(
        layout=go.Layout(
            title=go.layout.Title(
                text='Tiempo dedicado'
            )
        ))
    fig.add_trace(go.Box(y=timesNoExp, x=levels,  # replace with your own data source
                         boxpoints='all',
                         pointpos=0,
                         fillcolor='rgba(0,0,0,0.1)',
                         name='Sin Experiencia'))
    fig.add_trace(go.Box(y=timesExp, x=levels,  # replace with your own data source
                         boxpoints='all',
                         pointpos=0,
                         fillcolor='rgba(0,0,0,0.1)',
                         name='Con Experiencia'))
    fig.update_xaxes(
        ticktext=levelsNames,
        tickvals=vals)

    fig.update_layout(
        yaxis_title='Tiempo',
        boxmode='group'  # group together boxes of the different traces for each value of x
    )
    return fig


@app.callback(
    Output("graphTriesCompare", "figure"),
    Input("dropdown", "value"))
def buggaBugga(color):
    fig = go.Figure(
        layout=go.Layout(
            title=go.layout.Title(
                text='Intentos por nivel'
            )
        ))
    fig.add_trace(go.Box(y=triesNoExp, x=levels,  # replace with your own data source
                         boxpoints='all',
                         pointpos=0,
                         fillcolor='rgba(0,0,0,0.1)',
                         name='Sin Experiencia'))
    fig.add_trace(go.Box(y=triesExp, x=levels,  # replace with your own data source
                         boxpoints='all',
                         pointpos=0,
                         fillcolor='rgba(0,0,0,0.1)',
                         name='Con Experiencia'))
    fig.update_xaxes(
        ticktext=levelsNames,
        tickvals=vals)

    fig.update_layout(
        yaxis_title='Intentos',
        boxmode='group'  # group together boxes of the different traces for each value of x
    )
    return fig


@app.callback(
    Output("graphCodeLengthCompare", "figure"),
    Input("dropdown", "value"))
def buggaBugga(color):
    fig = go.Figure(
        layout=go.Layout(
            title=go.layout.Title(
                text='Longitud del Codigo'
            )
        ))

    fig.add_trace(go.Box(y=codeLengthNoExp, x=levels,  # replace with your own data source
                         boxpoints='all',
                         pointpos=0,
                         fillcolor='rgba(0,0,0,0.1)',
                         name='Sin Experiencia'))
    fig.add_trace(go.Box(y=codeLengthExp, x=levels,  # replace with your own data source
                         boxpoints='all',
                         pointpos=0,
                         fillcolor='rgba(0,0,0,0.1)',
                         name='Con Experiencia'))

    fig.update_xaxes(
        ticktext=levelsNames,
        tickvals=vals)

    fig.update_layout(
        yaxis_title ='Longitud',
        boxmode='group'  # group together boxes of the different traces for each value of x
    )
    return fig


@app.callback(
    Output("graphHelpCompare", "figure"),
    Input("dropdown", "value"))
def buggaBugga(color):
    fig = go.Figure(data=[
        go.Bar(y=helps, x=levelsNames,  # replace with your own data source
               name='Helped'),
        go.Bar(y=notHelps, x=levelsNames,
               name='Not helped')],
        layout=go.Layout(
            title=go.layout.Title(
                text='Numero de Ayudas utilizadas'
            )
    ))
    fig.update_layout(barmode='stack')
    fig.update_yaxes(title="Usuarios")
    return fig


@app.callback(
    Output("graphOptimCompare", "figure"),
    Input("dropdown", "value"))
def buggaBugga(color):
    fig = go.Figure(
        layout=go.Layout(
            title=go.layout.Title(
                text='Soluciones óptimas'
            )
    ))


    data =  [optimExp, notOptimExp, optimNoExp, notOptimNoExp]
    names =  ["Optimo", "No Optimo"]

    for i in range(len(data)):
    ## put var1 and var2 together on the first subgrouped bar
        if i <= 1:
            fig.add_trace(
                go.Bar(x=[levelsNames, ['Sin Experiencia']*len(levels)], y=data[i], name=names[i%2]),
            )
        ## put var3 and var4 together on the first subgrouped bar
        else:
            fig.add_trace(
                go.Bar(x=[levelsNames, ['Con Experiencia']*len(levels)], y= data[i], name=names[i%2]),
            )


    fig.update_layout(barmode='stack')
    fig.update_yaxes(title="Usuarios")
    return fig



app.run_server(debug=True)