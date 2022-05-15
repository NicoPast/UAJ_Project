from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np
import json
from processData import getProbadores,agruparProbadores,separarProbadores

app = Dash(__name__)

# with open('path_to_file/person.json', 'r') as f:
#   data = json.load(f) # as dictionary


#Poblacion involucrada en las pruebas
Probadores=getProbadores()

#Pedimos los datos generales de todos los probadores
NivelesGeneral=agruparProbadores(Probadores)

#Pedirmos los datos de solamente aquellos probadores que tengan experiencia en la programación
NivelesExperiencia = agruparProbadores(separarProbadores(Probadores,"programador",True))

#Pedimos los datos de aquellos probadores que no tengan experiencia en la programación
NivelesSinExperiencia = agruparProbadores(separarProbadores(Probadores,"programador",False))

#Nombre de cada uno de los niveles que se han probado
levelsNames = np.array(list(NivelesGeneral.keys()))
numLevels = len(levelsNames)
vals = [i for i in range(numLevels)]


#Variables involucradas en obtener los datos de todos los usuarios
playTime = []
intentos = []
longCodigo = []
sinAyudas = []
solOptima = []
for i in range(len(NivelesGeneral)):
    playTime.append(np.array(list(NivelesGeneral.values())[i]['playTime']))
    intentos.append(np.array(list(NivelesGeneral.values())[i]['tries']))
    longCodigo.append(np.array(list(NivelesGeneral.values())[i]['codeLength']))
    sinAyudas.append(np.array(list(NivelesGeneral.values())[i]['noHints']))
    solOptima.append(np.array(list(NivelesGeneral.values())[i]['codeOptimo']))

#Variables involucradas en obtener los datos solo de los usuarios con experiencia en la programación
playTimeExperimentados = []
intentosExperimentados = []
longCodigoExperimentados = []
sinAyudasExperimentados = []
solOptimaExperimentados = []
for i in range(len(NivelesExperiencia)):
    playTimeExperimentados.append(np.array(list(NivelesExperiencia.values())[i]['playTime']))
    intentosExperimentados.append(np.array(list(NivelesExperiencia.values())[i]['tries']))
    longCodigoExperimentados.append(np.array(list(NivelesExperiencia.values())[i]['codeLength']))
    sinAyudasExperimentados.append(np.array(list(NivelesExperiencia.values())[i]['noHints']))
    solOptimaExperimentados.append(np.array(list(NivelesExperiencia.values())[i]['codeOptimo']))

#Variables involucradas en obtener los datos solo de los usuarios que no experiencia en la programación
playTimeNoExperimentados = []
intentosNoExperimentados = []
longCodigoNoExperimentados = []
sinAyudasNoExperimentados = []
solOptimaNoExperimentados = []
for i in range(len(NivelesSinExperiencia)):
    playTimeNoExperimentados.append(np.array(list(NivelesSinExperiencia.values())[i]['playTime']))
    intentosNoExperimentados.append(np.array(list(NivelesSinExperiencia.values())[i]['tries']))
    longCodigoNoExperimentados.append(np.array(list(NivelesSinExperiencia.values())[i]['codeLength']))
    sinAyudasNoExperimentados.append(np.array(list(NivelesSinExperiencia.values())[i]['noHints']))
    solOptimaNoExperimentados.append(np.array(list(NivelesSinExperiencia.values())[i]['codeOptimo']))



#Metodo que recibe un array de arrays y a partir de cada elemetos de los subarrays genera unas coordenadas dependiendo de en qué subarray se encuentre cada elemento
def sacarCoordenadas(valores):
    coordenadasX= np.array([])
    coordenadasY = np.array([])
    i =0
    for elem in valores:
        
        for value in elem:
            coordenadasX = np.append(coordenadasX,i)
            coordenadasY = np.append(coordenadasY, value)
        i+=1
    return coordenadasX,coordenadasY


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
    coordenadasX, coordenadasY = sacarCoordenadas(playTime)
    fig = go.Figure(
        data=go.Box(y=coordenadasY, x=coordenadasX,  # replace with your own data source
                    boxpoints='all',
                    pointpos=0,
                    fillcolor='rgba(0,0,0,0.1)',
                    # marker_color=color,
                    name='Valores de tiempo'),
        layout=go.Layout(
            title=go.layout.Title(
                text='Tiempo dedicado'
            )
        ))

    fig.add_trace(go.Scatter(x=vals, y=[np.average(playTime[i]) for i in range(numLevels)], name='Tiempo medio'))

    fig.update_xaxes(
        ticktext=levelsNames,
        tickvals=vals)
    fig.update_yaxes(title="Tiempo")
    return fig


@app.callback(
    Output("graphTries", "figure"),
    Input("dropdown", "value"))
def buggaBugga(color):
    coordenadasX, coordenadasY = sacarCoordenadas(intentos)
    fig = go.Figure(
        data=go.Box(y=coordenadasY, x=coordenadasX,  # replace with your own data source
                    boxpoints='all',
                    pointpos=0,
                    fillcolor='rgba(0,0,0,0.1)',
                    # marker_color=color,
                    name='Valores de nº intentos'),
        layout=go.Layout(
            title=go.layout.Title(
                text='Intentos por nivel'
            )
        ))

    a = [np.average(intentos[i]) for i in range(numLevels)]
    fig.add_trace(go.Scatter(x=vals, y=[np.average(intentos[i]) for i in range(numLevels)],
                             name='Nº medio de intentos'))
    fig.update_xaxes(
        ticktext=levelsNames,
        tickvals=vals)
    fig.update_yaxes(title="Intentos")
    return fig


@app.callback(
    Output("graphCodeLength", "figure"),
    Input("dropdown", "value"))
def buggaBugga(color):
    coordenadasX, coordenadasY = sacarCoordenadas(longCodigo)
    fig = go.Figure(
        data=go.Box(y=coordenadasY, x=coordenadasX,  # replace with your own data source
                    boxpoints='all',
                    pointpos=0,
                    fillcolor='rgba(0,0,0,0.1)',
                    # marker_color=color,
                    name='Valores de longitud de código'),
        layout=go.Layout(
            title=go.layout.Title(
                text='Longitud del código'
            )
        ))
    a = [np.average(longCodigo[i]) for i in range(numLevels)]
    fig.add_trace(go.Scatter(x=vals, y=[np.average(longCodigo[i]) for i in range(numLevels)],
                             name='Longitud media de código'))
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
        go.Bar(y=np.array([ len(sinAyudas[i]) - np.sum(sinAyudas[i]) for i in range(numLevels)]), x=levelsNames,  # replace with your own data source
               name='Necesitó ayuda'),
        go.Bar(y=np.array([ np.sum(sinAyudas[i]) for i in range(numLevels)]), x=levelsNames,
               name='NO necesitó ayuda')],
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
        go.Bar(y=np.array([ np.sum(solOptima[i]) for i in range(numLevels)]), x=levelsNames,  # replace with your own data source
               name='Solución óptima'),
        go.Bar(y=np.array([ len(solOptima[i]) - np.sum(solOptima[i]) for i in range(numLevels)]), x=levelsNames,
               name='Solución NO óptima')],
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
    coordenadasX, coordenadasY = sacarCoordenadas(playTimeExperimentados)
    fig.add_trace(go.Box(y=coordenadasY, x=coordenadasX,  # replace with your own data source
                         boxpoints='all',
                         pointpos=0,
                         fillcolor='rgba(0,0,0,0.1)',
                         name='Sin experiencia'))
    coordenadasX, coordenadasY = sacarCoordenadas(playTimeNoExperimentados)
    fig.add_trace(go.Box(y=coordenadasY, x=coordenadasX,  # replace with your own data source
                         boxpoints='all',
                         pointpos=0,
                         fillcolor='rgba(0,0,0,0.1)',
                         name='Con experiencia'))
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
    coordenadasX, coordenadasY = sacarCoordenadas(intentosNoExperimentados)
    fig.add_trace(go.Box(y=coordenadasY, x=coordenadasX,  # replace with your own data source
                         boxpoints='all',
                         pointpos=0,
                         fillcolor='rgba(0,0,0,0.1)',
                         name='Sin experiencia'))

    coordenadasX, coordenadasY = sacarCoordenadas(intentosExperimentados)                       
    fig.add_trace(go.Box(y=coordenadasY, x=coordenadasX,  # replace with your own data source
                         boxpoints='all',
                         pointpos=0,
                         fillcolor='rgba(0,0,0,0.1)',
                         name='Con experiencia'))
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

    coordenadasX, coordenadasY = sacarCoordenadas(longCodigoNoExperimentados)
    fig.add_trace(go.Box(y=coordenadasY, x=coordenadasX,  # replace with your own data source
                         boxpoints='all',
                         pointpos=0,
                         fillcolor='rgba(0,0,0,0.1)',
                         name='Sin experiencia'))

    coordenadasX, coordenadasY = sacarCoordenadas(longCodigoExperimentados)
    fig.add_trace(go.Box(y=coordenadasY, x=coordenadasX,  # replace with your own data source
                         boxpoints='all',
                         pointpos=0,
                         fillcolor='rgba(0,0,0,0.1)',
                         name='Con experiencia'))

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
        #Para los que SI TIENEN EXPERIENCIA
        go.Bar(y=np.array([ len(sinAyudasExperimentados[i]) - np.sum(sinAyudasExperimentados[i]) for i in range(len(sinAyudasExperimentados))]), x=levelsNames,  # replace with your own data source
               name='Necesitó ayuda y tenía experiencia'),
        go.Bar(y=np.array([ np.sum(sinAyudasExperimentados[i]) for i in range(len(sinAyudasExperimentados))]), x=levelsNames,
               name='NO necesitó ayuda y tenía experiencia'),

        #para los que NO TIENEN EXPERIENCIA
        go.Bar(y=np.array([ len(sinAyudasNoExperimentados[i]) - np.sum(sinAyudasNoExperimentados[i]) for i in range(len(sinAyudasNoExperimentados))]), x=levelsNames,  # replace with your own data source
               name='Necesitó ayuda y NO tenía experiencia'),
        go.Bar(y=np.array([ np.sum(sinAyudasNoExperimentados[i]) for i in range(len(sinAyudasNoExperimentados))]), x=levelsNames,
               name='NO necesitó ayuda y NO tenía experiencia')],
               
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


    # data =  [optimExp, notOptimExp, optimNoExp, notOptimNoExp]
    data =  [np.array([ np.sum(solOptimaExperimentados[i]) for i in range(len(solOptimaExperimentados))]), 
            np.array([ len(solOptimaExperimentados[i]) - np.sum(solOptimaExperimentados[i]) for i in range(len(solOptimaExperimentados))]), 
            np.array([ np.sum(solOptimaNoExperimentados[i]) for i in range(len(solOptimaNoExperimentados))]), 
            np.array([ len(solOptimaNoExperimentados[i]) - np.sum(solOptimaNoExperimentados[i]) for i in range(len(solOptimaNoExperimentados))])]
    names =  ["Óptimo", "No Óptimo"]

    for i in range(len(data)):
    ## put var1 and var2 together on the first subgrouped bar
        if i <= 1:
            fig.add_trace(
                go.Bar(x=[levelsNames, ['Con experiencia']*numLevels], y=data[i], name=names[i%2]),
            )
        ## put var3 and var4 together on the first subgrouped bar
        else:
            fig.add_trace(
                go.Bar(x=[levelsNames, ['Sin experiencia']*numLevels], y= data[i], name=names[i%2]),
            )


    fig.update_layout(barmode='stack')
    fig.update_yaxes(title="Usuarios")
    return fig



app.run_server(debug=True)
