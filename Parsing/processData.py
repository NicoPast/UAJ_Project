import operator
from Parsing import hacerDiccionario



def main():

    trazas = hacerDiccionario()
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
            #Comprobación de que existe y tal
            nombreNivel = succesfull["object"]["id"]
            timestamp = succesfull["timestamp"]

            #Aumentamos contador con el número de veces que se ha completado cada nivel
            Probadores[nombreProbador][nombreNivel].intentos =  Probadores[nombreProbador][nombreNivel].intentos+1
            duracionesNiveles.append({nombreNivel, timestamp})


        for failed in trazas[nombreProbador]["FailedLevels"]:
            #Comprobación de que existe y tal
            nombreNivel = failed["object"]["id"]
            timestamp = failed["timestamp"]

            #Aumentamos contador con los intentos fallidos de dicho nivel
            Probadores[nombreProbador][nombreNivel].intentos =  Probadores[nombreProbador][nombreNivel].intentos+1
            duracionesNiveles.append({nombreNivel, timestamp})


    ################################# Longitud del código  #####################################
        for intento in trazas[nombreProbador]["LevelTries"]:
            #Comprobación de que existe y tal
            nombreNivel = intento["object"]["id"]

            #Obtenemos el codigo de la ultima vez que se ejecutó el nivel y calculamos su longitud
            codigo = intento["result"]["extensions"]["code"]
            Probadores[nombreProbador][nombreNivel].longitudCodigo =  0 #calculo de la hostia


    ################################# Duracion de cada nivel #####################################
        #Ordenar el array
        duracionesNiveles.sort(key=operator.attrgetter('timestamp'))
        pos = 10
        while pos !=0:
            duracionNivelActual=0
            nivelAAnalizar = duracionesNiveles[pos].nombreNivel
            while duracionesNiveles[pos-1].nombreNivel == nivelAAnalizar:
                duracionNivelActual+= 10 #calculo de parsear de string a numeros 
                pos = pos-1
            
            Probadores[nombreProbador][nombreNivel].duracion = duracionNivelActual








