import json

'''
Notas(Ricky y Ana): Eventos que hacen falta
    Comienzo de un nivel

    Intentos de nivel

    Final de un nivel

Como parseamos:    
Sintaxis general:
    verb
        id
            http://adlnet.gov/expapi/verbs/progressed
    object
        definition
            type
                https://w3id.org/xapi/seriousgames/activity-types/level

Notas de Ricky y Ana para las medias:
    * Duración de nivel: timestamp de evento de final - timestamp de evento de inicio, por nivel (trace['object']['id'])
    * Número de intentos por nivel: sumar n de success + n de failed, por nivel 
    * Longitud de código de niveles acertados: 
        * Asociar el acierto con el intento correspondiente (tienen el mismo nivel) para sacar el código (trace['result']['extensions'])
        * Del código, parsear xml para contar bloques y hacer la media
        * Otra vez, todo esto por cada nivel 

Si pueden saquen medias divididas por las dos demográficas (programadores y no programadores)
'''

TRACES_FILE = "./traces.json"

user_traces = {}
    
def ensure_user(trace):
    name = trace['actor']['name']
    if not name in user_traces:
        user_traces[name] = {'Name':name,'LevelTries':{}, 'SuccessLevels':[], 'FailedLevels':[]}
    return name

def filter(objs):
    for obj in objs:
        obj.pop('actor')
        obj.pop('verb')
        obj.pop('_id')
        obj['object'].pop('definition')
        if'result' in obj and 'score' in obj['result']:
            obj['result'].pop('score')
        if'result' in obj and 'success' in obj['result']:
            obj['result'].pop('success')
        obj['object']['id'] = obj['object']['id'].split("/")[-1]
    return objs

def hacerDiccionario():
    with open(TRACES_FILE) as traces:
        all_traces = json.loads(traces.read())    
        for trace in all_traces:
            valid = ('verb' in trace and 'id' in trace['verb'] and 'object' in trace and 'definition' in trace['object'] and 'type' in trace['object']['definition'])
            if(valid):
                user = ensure_user(trace)
                if(trace['verb']['id']=='http://adlnet.gov/expapi/verbs/progressed' and trace['object']['definition']['type']=="https://w3id.org/xapi/seriousgames/activity-types/level"):
                    user_traces[user]['LevelTries'][trace['object']['id'].split('/')[-1]]=trace
                if(trace['verb']['id'] == 'http://adlnet.gov/expapi/verbs/completed' and trace['object']['definition']['type']=='https://w3id.org/xapi/seriousgames/activity-types/level'):
                    user_traces[user]['SuccessLevels' if trace['result']['success'] else 'FailedLevels'].append(trace)
    
    return user_traces


def printTraces(user_traces):
    print("[")
    for key in user_traces.keys():
        
        #Convert sets(dicts) to lists
        user_traces[key]['LevelTries'] = list(user_traces[key]['LevelTries'].values())

        #Sort
        user_traces[key]['LevelTries'].sort(key=lambda x: x['timestamp'])
        user_traces[key]['FailedLevels'].sort(key=lambda x: x['timestamp'])
        user_traces[key]['SuccessLevels'].sort(key=lambda x: x['timestamp'])

        #Filters
        user_traces[key]['LevelTries'] = filter(user_traces[key]['LevelTries'])
        user_traces[key]['FailedLevels'] = filter(user_traces[key]['FailedLevels'])
        user_traces[key]['SuccessLevels'] = filter(user_traces[key]['SuccessLevels'])

        print(json.dumps(user_traces[key], indent=4))
        if(key != list(user_traces.keys())[-1]):
            print(',')
    print("]")


def main():
    printTraces(hacerDiccionario())
    

if __name__ == "__main__":
    main()