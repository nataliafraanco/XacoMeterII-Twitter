import pandas as pd #Para poder almacenar datos en dataframes
#import pyodbc #Proporciona herramientas para conectarse a una base de datos SQL
import credencialesAPITwitter
import requests
import json
import csv
import dateutil.parser


def auth():
    return credencialesAPITwitter.BEARER_TOKEN

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def create_url(keyword, max_results):
    
    endpoint_url = "https://api.twitter.com/2/tweets/search/recent"

    #change params based on the endpoint you are using
    query_parameters = {'query': keyword,
                    'max_results': max_results,
                    'tweet.fields': 'id,text,author_id,created_at,lang',
                    'user.fields': 'id,name,username,verified',
                    'place.fields': 'country,country_code,full_name,geo,name',
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
    json_response = connect_to_endpoint(url[0], headers, url[1])
    #print(json.dumps(json_response, indent=4, sort_keys=True))
    return json_response
    
def insert_data(json_response, fileName):

    #A counter variable
    cont = 0

    #Open OR create the target CSV file
    csvFile = open(fileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Loop through each tweet
    for tweet in json_response['data']:
        
        author_id = tweet['author_id']
        created_at = dateutil.parser.parse(tweet['created_at'])
        if ('geo' in tweet):   
            geo = tweet['geo']['place_id']
        else:
            geo = " "
        tweet_id = tweet['id']
        lang = tweet['lang']
        text = tweet['text']

        res = [author_id, created_at, geo, tweet_id, lang, text]
        
        # Append the result to the CSV file
        csvWriter.writerow(res)
        cont += 1

    # When done, close the CSV file
    csvFile.close()

    # Print the number of tweets for this iteration
    return cont 

