import pandas as pd #Para poder almacenar datos en dataframes
#import pyodbc #Proporciona herramientas para conectarse a una base de datos SQL
import credencialesAPITwitterEducative
import requests
import json
import csv
import dateutil.parser
import psycopg2


def auth():
    return credencialesAPITwitterEducative.BEARER_TOKEN

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def create_url(keyword, max_results):
    
    endpoint_url = "https://api.twitter.com/2/tweets/search/all"

    #change params based on the endpoint you are using
    query_parameters = {'query': keyword,
                    'max_results': max_results,
                    'expansions': 'author_id,geo.place_id',
                    'tweet.fields': 'id,text,author_id,created_at,lang,public_metrics,geo',
                    'user.fields': 'id,name,username,verified',
                    'place.fields': 'country',
                    'next_token': {}
                    }
    
    return (endpoint_url, query_parameters)

def connect_to_endpoint(url, headers, parameters, next_token = None):
    parameters['next_token'] = next_token  
    response = requests.request("GET", url, headers = headers, params = parameters)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def principal_function(PalabraClave):
    #Inputs for the request
    bearer_token = auth()
    headers = create_headers(bearer_token)
    keyword = PalabraClave
    max_results = 100
    url = create_url(keyword, max_results)
    dict_tweets = connect_to_endpoint(url[0], headers, url[1])
    print(json.dumps(dict_tweets, indent=4, sort_keys=True))
    return dict_tweets
    
def insert_data(json_response, fileName):

    #A counter variable
    cont = 0

    #Open OR create the target CSV file
    csvFile = open(fileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Loop through each tweet
    for tweet, user in zip (json_response['data'], json_response['includes']['users']):
        
        author_id = tweet['author_id']
        #username = tweet['includes_users']['username']
        created_at = dateutil.parser.parse(tweet['created_at'])
        username = user['username']
        if ('geo' in tweet):   
            geo = tweet['geo']
        else:
            geo = "No hay geolocalización"
        tweet_id = tweet['id']
        lang = tweet['lang']
        text = tweet['text']
        retweet_count = tweet['public_metrics']['retweet_count']
        like_count = tweet['public_metrics']['like_count']
        reply_count = tweet['public_metrics']['reply_count']
        res = [author_id, created_at, username, geo, tweet_id, lang, text, retweet_count, like_count,reply_count]
        
        # Append the result to the CSV file
        csvWriter.writerow(res)
        cont += 1

    # When done, close the CSV file
    csvFile.close()
    return pd.read_csv('Catedral_Burgos.csv', header =None, names = ['author_id', 'created_at', 'username', 'geo', 'tweet_id', 'lang', 'text', 'retweet_count', 'like_count','reply_count']) #No importan mayusculas ni si las palabras estan separadas en el tweet.
    # Print the number of tweets for this iteration
    #return cont 

