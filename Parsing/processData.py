from email.utils import formatdate
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
    codeLenght=0

#Clase que recopila la información de un probador 
class Tester:
    #Si ha recibido clases de programacion o no
    programador = False
    #Diccionario que tiene una entrada por nivel jugado con informacion de su desempeño en cada uno
    infoLevels = dict()

    def __init__(self):
        self.programador=False
        self.infoLevels= dict()

class Media:
    contador = 0
    acumulador=0

    def __init__(self, cont, acum):
        self.contador=cont
        self.acumulador= acum




def mediaIntentos(poblacion):
    #Diccionario auxiliar para calcular las medias
    mediasNiveles = dict()

    #Recorremos cada individuo dentro de la poblacion
    for individuo in poblacion:

        #Para cada individuo miramos todos los niveles que este haya jugado
        for nivelJugado in poblacion[individuo].infoLevels:
            #En caso de que en nuestro diccionario auxiliar no exista este nivel lo añadimos con los datos del probador
            if(not nivelJugado in mediasNiveles):            
                mediasNiveles[nivelJugado] = Media(1, poblacion[individuo].infoLevels[nivelJugado].tries)
            #Si sí existe añadimos 1 al número de personas que lo han jugado y añadimos el número de intentos que ha hecho este probador
            else:
                mediasNiveles[nivelJugado].contador = mediasNiveles[nivelJugado].contador+1
                mediasNiveles[nivelJugado].acumulador += poblacion[individuo].infoLevels[nivelJugado].tries

    #Para devolver los datos devolvemos otro diccionario en el que se tratan los datos que se han acumulado
    medias = dict()
    for clave in mediasNiveles:
        medias[clave] = mediasNiveles[clave].acumulador / mediasNiveles[clave].contador
    return medias




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

            #Pasamos la fecha del evento a un timestamp util para nosotros
            format_date = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
            converted_timestamp=format_date.timestamp()

            #Aumentamos contador con el número de veces que se ha completado cada nivel
            Probadores[nombreProbador].infoLevels[nombreNivel].startTime =  converted_timestamp

        #Recorremos los niveles en los que haya fallado
        for failed in trazas[nombreProbador]["FailedLevels"]:
            nombreNivel = failed["object"]["id"]
            timestamp = failed["timestamp"]
            #En caso de que no tenga info sobre este nivel se la añadimos
            if(not nombreNivel in Probadores[nombreProbador].infoLevels):            
                Probadores[nombreProbador].infoLevels[nombreNivel]=levelInfo()

            #Pasamos la fecha del evento a un timestamp util para nosotros
            format_date = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
            converted_timestamp=format_date.timestamp()

            #Aumentamos contador con el número de veces que se ha completado cada nivel
            Probadores[nombreProbador].infoLevels[nombreNivel].tries =  Probadores[nombreProbador].infoLevels[nombreNivel].tries+1


    ################################# Longitud del código  #####################################
        #Por cada nivel jugado miramos el codigo que mandó y contamos los bloques que lo forman
        for intento in trazas[nombreProbador]["LevelTries"]:
            nombreNivel = intento["object"]["id"]

            #En caso de que no tenga info sobre este nivel se la añadimos
            if(not nombreNivel in Probadores[nombreProbador].infoLevels):            
                Probadores[nombreProbador].infoLevels[nombreNivel]=levelInfo()

            #Obtenemos el codigo de la ultima vez que se ejecutó el nivel y calculamos su longitud
            codigo = intento["result"]["extensions"]["code"]
            xml= ET.ElementTree(ET.fromstring(codigo))
            #Por cada aparicion del bloque 'block' aumentamos el contador de instrucciones
            instructions=0
            for block in xml.iter('block'):
                instructions+=1
            Probadores[nombreProbador].infoLevels[nombreNivel].codeLenght = instructions 

        #Niveles que ha completado correctamente
        for succesfull in trazas[nombreProbador]["SuccessLevels"]:
            nombreNivel = succesfull["object"]["id"]
            timestamp = succesfull["timestamp"]
            #En caso de que no tenga info sobre este nivel se la añadimos
            if(not nombreNivel in Probadores[nombreProbador].infoLevels):            
                Probadores[nombreProbador].infoLevels[nombreNivel]=levelInfo()

            #Pasamos la fecha del evento a un timestamp util para nosotros
            format_date = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
            converted_timestamp=format_date.timestamp()

            #Aumentamos contador con el número de veces que se ha completado cada nivel
            Probadores[nombreProbador].infoLevels[nombreNivel].tries =  Probadores[nombreProbador].infoLevels[nombreNivel].tries+1
            Probadores[nombreProbador].infoLevels[nombreNivel].playTime =  converted_timestamp - Probadores[nombreProbador].infoLevels[nombreNivel].startTime
            Probadores[nombreProbador].infoLevels[nombreNivel].levelWasCompleted =  True

    #############Obtención de programadores o no programadores (estan en otro fichero)
    #Leemos el csv entero
    datosCSV=[]
    with open('results-survey945759.csv', 'r') as file:
        #Como delimitador ponemos los ;
        reader = csv.reader(file,delimiter=';')
        for each_row in reader:
            datosCSV.append(each_row)

    columnaProgramacion = 5
    #Sacar quien es programador o no de todos los probadores
    for pos in range(1,len(datosCSV)):
        if datosCSV[pos][columnaProgramacion] == "No":
            Probadores[datosCSV[pos][1]].programador = False
        else:
            Probadores[datosCSV[pos][1]].programador = True
    
    
####################
    mediaIntentos(Probadores)






main()





