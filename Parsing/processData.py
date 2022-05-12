from email.utils import formatdate
import operator
from Parsing import hacerDiccionario,prettify
from datetime import datetime
import xml.etree.ElementTree as ET
class levelInfo:
    tries=0
    playTime=0
    codeLenght=0
class timeInfo:
    levelName = ""
    levelTime = 0   
    def __init__(self,name,time):
        self.levelName=name
        self.levelTime=time


def main():

    trazas = prettify(hacerDiccionario())
    #Sacar el número de niveles que hay
    #Diccionario una entrada por persona => pepito que tiene una entrada por nivel => {info: {tiempo tardado, num intentos, cosas pistas, cosas código, " sabe de programación o no"}}
    numPersonas = 100
    Probadores = {}

    #Por cada persona recorro todos los niveles
    for nombreProbador in trazas.keys():

        #Preparar diccionario
        Probadores[nombreProbador]= dict()
        duracionesNiveles = [] 

    #################################Número de intentos por nivel: sumar n de success + n de failed, por nivel #####################################
        for succesfull in trazas[nombreProbador]["SuccessLevels"]:
            
            nombreNivel = succesfull["object"]["id"]
            timestamp = succesfull["timestamp"]
            if(not nombreNivel in Probadores[nombreProbador]):            
                Probadores[nombreProbador][nombreNivel]=levelInfo()
            format_date = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
            converted_timestamp=format_date.timestamp()
            #Aumentamos contador con el número de veces que se ha completado cada nivel
            Probadores[nombreProbador][nombreNivel].tries =  Probadores[nombreProbador][nombreNivel].tries+1
            duracionesNiveles.append(timeInfo(nombreNivel, converted_timestamp))


        for failed in trazas[nombreProbador]["FailedLevels"]:
            #Comprobación de que existe y tal
            nombreNivel = failed["object"]["id"]
            timestamp = failed["timestamp"]
            if(not nombreNivel in Probadores[nombreProbador]):            
                Probadores[nombreProbador][nombreNivel]=levelInfo()

            #Aumentamos contador con los intentos fallidos de dicho nivel
            format_date = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
            converted_timestamp=format_date.timestamp()
            Probadores[nombreProbador][nombreNivel].tries =  Probadores[nombreProbador][nombreNivel].tries+1
            duracionesNiveles.append(timeInfo(nombreNivel, converted_timestamp))


    ################################# Longitud del código  #####################################
        for intento in trazas[nombreProbador]["LevelTries"]:
            #Comprobación de que existe y tal
            nombreNivel = intento["object"]["id"]
            if(not nombreNivel in Probadores[nombreProbador]):            
                Probadores[nombreProbador][nombreNivel]=levelInfo()

            #Obtenemos el codigo de la ultima vez que se ejecutó el nivel y calculamos su longitud
            codigo = intento["result"]["extensions"]["code"]
            xml= ET.ElementTree(ET.fromstring(codigo))
            cont=0
            for block in xml.iter('block'):
                cont+=1
            Probadores[nombreProbador][nombreNivel].codeLenght =cont #calculo de la hostia


    ################################# Duracion de cada nivel #####################################
    #Ordenar el array
        duracionesNiveles.sort(key=operator.attrgetter('levelTime'))
        pos = len(duracionesNiveles)-1
        nivelAAnalizar=""
        while pos != 0 and nivelAAnalizar != duracionesNiveles[0].levelName:
            duracionNivelActual=0
            nivelAAnalizar = duracionesNiveles[pos].levelName
            while duracionesNiveles[pos-1].levelName == nivelAAnalizar:
                duracionNivelActual+= Probadores[nombreProbador][nivelAAnalizar].playTime #calculo de parsear de string a numeros 
                pos = pos-1
            

    a=2


main()





