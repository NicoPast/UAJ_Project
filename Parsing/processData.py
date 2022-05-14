from email.utils import formatdate
from pytest import param
from sklearn.metrics import median_absolute_error
from sqlalchemy import false
from Parsing import hacerDiccionario,prettify
from datetime import datetime
import xml.etree.ElementTree as ET
import csv


#Clase que representa la info de un Nivel que ha realizado un Probador
class levelInfo:
    tries=0
    startTime=0
    playTime=0
    levelWasCompleted=False
    noHints=False
    codeLength=0

#Clase que recopila la información de un probador 
class Tester:
    #Si ha recibido clases de programacion o no
    programador = False
    genero = "Otro"
    #Diccionario que tiene una entrada por nivel jugado con informacion de su desempeño en cada uno
    infoLevels = dict()

    def __init__(self):
        self.programador=False
        self.infoLevels= dict()

#Clase auxiliar para sacar medias
class Media:
    contador = 0
    acumulador=0

    def __init__(self, cont, acum):
        self.contador=cont
        self.acumulador= acum


##Este método tiene como objetivo tomar la población y seleccionar aquellos individuos cuyo parámetro especificado sea igual al valor dado
#El método devuelve la sección de la población que cumple con dichos requisitos
def separarAlumnos(poblacion,parametro,  valor):
    result = dict()
    for elem in poblacion:
        if(getattr(poblacion[elem],parametro) == valor):
            result[elem] = poblacion[elem]

    return result

#Metodo que toma una poblacion que ha jugado una serie de niveles y calcula la media a partir del nombre 
# de un parámetro que se pasa teniendo en cuenta si es necesario o no que el usuario haya completado el nivel
def mediaSegunParametro(poblacion, parametro, soloNivelesCompletados):
    #Diccionario auxiliar para calcular las medias
    mediasNiveles = dict()

    #Recorremos cada individuo dentro de la poblacion
    for individuo in poblacion:
        #Para cada individuo miramos todos los niveles que este haya jugado
        for nivelJugado in poblacion[individuo].infoLevels:

            #En caso de que en nuestro diccionario auxiliar no exista este nivel lo añadimos dependiendo de si es necesario que el probador haya completado el nivel o no
            levelCompleted = poblacion[individuo].infoLevels[nivelJugado].levelWasCompleted
            if(not nivelJugado in mediasNiveles and ((levelCompleted and soloNivelesCompletados) or (not soloNivelesCompletados))):            
                mediasNiveles[nivelJugado] = Media(1, getattr(poblacion[individuo].infoLevels[nivelJugado],parametro))

            #Si sí existe añadimos 1 al número de personas que lo han jugado y añadimos el número de intentos que ha hecho este probador
            elif ((levelCompleted and soloNivelesCompletados) or (not soloNivelesCompletados)):
                mediasNiveles[nivelJugado].contador = mediasNiveles[nivelJugado].contador+1
                mediasNiveles[nivelJugado].acumulador += getattr(poblacion[individuo].infoLevels[nivelJugado],parametro)

    #Para devolver los datos devolvemos otro diccionario en el que se tratan los datos que se han acumulado
    medias = dict()
    for clave in mediasNiveles:
        medias[clave] = mediasNiveles[clave].acumulador / mediasNiveles[clave].contador
    return medias


#MEtodo para transformar las fechas almacenadas en las trazas a timestaps EPOCH
def timeToEpoch(date):
    format_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f%z')
    converted_timestamp=format_date.timestamp()
    return converted_timestamp

def main():

    #Obtenemos las trazas limpias sobre los probadores de una sesion
    trazas = prettify(hacerDiccionario())
    #Dicccionario que va a tener una entrada por probador
    Probadores = {}

    #Recorremos todas las personas de las trazas
    for nombreProbador in trazas.keys():
        Probadores[nombreProbador]= Tester()

    #################################Número de intentos por nivel: sumar n de success + n de failed, por nivel #####################################

        #Niveles que ha completado correctamente
        for initialized in trazas[nombreProbador]["InitializedLevels"]:
            nombreNivel = initialized["object"]["id"]
            timestamp = initialized["timestamp"]
            #En caso de que no tenga info sobre este nivel se la añadimos
            if(not nombreNivel in Probadores[nombreProbador].infoLevels):            
                Probadores[nombreProbador].infoLevels[nombreNivel]=levelInfo()

            #Aumentamos contador con el número de veces que se ha completado cada nivel
            Probadores[nombreProbador].infoLevels[nombreNivel].startTime = timeToEpoch(timestamp)

        #Recorremos los niveles en los que haya fallado
        for failed in trazas[nombreProbador]["FailedLevels"]:
            nombreNivel = failed["object"]["id"]
            #En caso de que no tenga info sobre este nivel se la añadimos
            if(not nombreNivel in Probadores[nombreProbador].infoLevels):            
                Probadores[nombreProbador].infoLevels[nombreNivel]=levelInfo()

            #Aumentamos contador con el número de veces que se ha completado cada nivel
            Probadores[nombreProbador].infoLevels[nombreNivel].tries =  Probadores[nombreProbador].infoLevels[nombreNivel].tries+1


    ################################# Longitud del código  #####################################
        #Por cada nivel jugado miramos el codigo que mandó y contamos los bloques que lo forman
        for intento in trazas[nombreProbador]["LevelTries"]:
            #En caso de que no tenga info sobre este nivel se la añadimos
            nombreNivel = intento["object"]["id"]
            if(not nombreNivel in Probadores[nombreProbador].infoLevels):            
                Probadores[nombreProbador].infoLevels[nombreNivel]=levelInfo()

            #Obtenemos el codigo de la ultima vez que se ejecutó el nivel y calculamos su longitud
            codigo = intento["result"]["extensions"]["code"]
            xml= ET.ElementTree(ET.fromstring(codigo))

            #Por cada aparicion del bloque 'block' aumentamos el contador de instrucciones
            instructions=0
            for block in xml.iter('block'):
                instructions+=1

            Probadores[nombreProbador].infoLevels[nombreNivel].codeLength = instructions 

        #Toma del momento en el que un jugador ha completado un nivel y cálculo del tiempo que ha tardado en completarlo
        for succesfull in trazas[nombreProbador]["SuccessLevels"]:
            nombreNivel = succesfull["object"]["id"]
            timestamp = succesfull["timestamp"]
            #En caso de que no tenga info sobre este nivel se la añadimos
            if(not nombreNivel in Probadores[nombreProbador].infoLevels):            
                Probadores[nombreProbador].infoLevels[nombreNivel]=levelInfo()

            #Aumentamos contador con el número de veces que se ha completado cada nivel
            Probadores[nombreProbador].infoLevels[nombreNivel].tries =  Probadores[nombreProbador].infoLevels[nombreNivel].tries+1
            Probadores[nombreProbador].infoLevels[nombreNivel].playTime =  timeToEpoch(timestamp) - Probadores[nombreProbador].infoLevels[nombreNivel].startTime
            Probadores[nombreProbador].infoLevels[nombreNivel].levelWasCompleted =  True
            Probadores[nombreProbador].infoLevels[nombreNivel].noHints =  succesfull["result"]["extensions"]["no_hints"]

    #############Obtención datos específicos de cada alumno (Programador/NoProgramador, Género)
    #Leemos el csv entero
    datosCSV=[]
    with open('results-survey945759.csv', 'r') as file:
        #Como delimitador ponemos los ;
        reader = csv.reader(file,delimiter=';')
        for each_row in reader:
            datosCSV.append(each_row)

    columnaProgramacion = 5
    columnaGenero = 8
    #Sacar quien es programador o no de todos los probadores
    for pos in range(1,len(datosCSV)):
        Probadores[datosCSV[pos][1]].genero = datosCSV[pos][columnaGenero]
        if datosCSV[pos][columnaProgramacion] == "No":
            Probadores[datosCSV[pos][1]].programador = False
        else:
            Probadores[datosCSV[pos][1]].programador = True
    
    
####################

    poblacionAAnalizar = separarAlumnos(Probadores,"programador", False)
    #Media de intentos que se han hecho en cada nivel
    mediaSegunParametro(Probadores,"tries",False )
    mediaSegunParametro(Probadores,"playTime",True )
    mediaSegunParametro(Probadores,"codeLength",True )



main()





