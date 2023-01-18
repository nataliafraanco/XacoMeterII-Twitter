import requests
import csv
import dateutil.parser
import logging
from datetime import datetime
import os

def auth():
    return os.getenv("BEARER_TOKEN")

def accederEncabezados(bearer_token):
    return {"Authorization": "Bearer {}".format(bearer_token)}

def solicitudURL(palabraClave, max_results, fecha, fechaFin):
    
    endpointUrl = "https://api.twitter.com/2/tweets/search/all"

    # Definir los parámetros que queremos obtener de la API de Twitter
    parametrosBusqueda = {'query': palabraClave,
                    'max_results': max_results,
                    'start_time': fecha,
                    'end_time': fechaFin,
                    'expansions': 'author_id,geo.place_id',
                    'tweet.fields': 'id,text,created_at,lang,public_metrics,geo',
                    'user.fields': 'username,verified',
                    'next_token': {}
                    }
    
    return (endpointUrl, parametrosBusqueda)

#Realizamos la conexión a la API y obtenemos la información deseada
def conexionEndpoint(url, headers, parameters, next_token = None):
    parameters['next_token'] = next_token  
    response = requests.request("GET", url, headers = headers, params = parameters)
    if response.status_code != 200:
        if response.status_code == 400:
            logging.error(f'{datetime.now()} - Twitter - Solicitud no valida')       
        elif response.status_code == 401:
            logging.error(f'{datetime.now()} - Twitter - Error de autenticacion')        
        elif response.status_code == 403:
            logging.error(f'{datetime.now()} - Twitter - Acceso denegado')        
        elif response.status_code == 429:
            logging.error(f'{datetime.now()} - Twitter - Solicitudes permitidas superadas')      
        else:
            logging.error(f'{datetime.now()} - Error de servidor')

        raise Exception(response.status_code, response.text)
    return response.json()

#Definimos las variables y hacemos las llamadas a las funciones
def funcionPrincipal(patrimonioId, PalabraClave, fecha, fechaFin):
    bearer_token = auth()
    headers = accederEncabezados(bearer_token)
    keyword = PalabraClave
    max_results = 500
    url = solicitudURL(keyword, max_results, fecha, fechaFin)
    dict_tweets = conexionEndpoint(url[0], headers, url[1])
    #print(json.dumps(dict_tweets, indent=4, sort_keys=True))
    return insertarDatosCSV(patrimonioId, dict_tweets)
    
#Creamos el fichero CSV y le rellenamos con la información
def insertarDatosCSV(patrimonioId, diccionarioTweets):

    #Añadimos el archivo CSV en una ruta temporal para que no tenga problemas en cuanto a permisos
    CSVPath = "data/temporal.csv"
    csvFile = open(CSVPath , "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)
    #Sacamos la información del archivo json y la añadimos linea a linea al archivo CSV
    if ('data' in diccionarioTweets)  :
        for tweet, usuario in zip (diccionarioTweets['data'], diccionarioTweets['includes']['users']):
            tweet_id = tweet['id']
            username = usuario['username']
            createdAt = dateutil.parser.parse(tweet['created_at'])
            if ('geo' in tweet):   
                geo = tweet['geo']
            else:
                geo = "No hay geolocalización"
            lang = tweet['lang']
            text = tweet['text']
            verified = usuario['verified']
            retweet_count = tweet['public_metrics']['retweet_count']
            like_count = tweet['public_metrics']['like_count']
            reply_count = tweet['public_metrics']['reply_count']
            lineaCSV = [patrimonioId, tweet_id, geo, lang, text, username, verified, retweet_count, like_count,reply_count, createdAt]
            csvWriter.writerow(lineaCSV)
        #Cerramos el fichero CSV
        csvFile.close()
        

