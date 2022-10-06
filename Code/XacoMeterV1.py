from flask import Flask, render_template
import tweepy
import credencialesAPI
from os import remove
import os

#Para saber donde buscar los archivos
app = Flask(__name__)

auth = tweepy.OAuth1UserHandler(
   credencialesAPI.API_KEY,
   credencialesAPI.API_KEY_SECRET,
   credencialesAPI.ACCESS_TOKEN,
   credencialesAPI.ACCESS_TOKEN_SECRET
)

api = tweepy.API(auth)
client = tweepy.Client (bearer_token = credencialesAPI.BEARER_TOKEN)

def BusquedaTweets(PalabraClave):

	#query = ('#%s -is:retweet lang:es', PalabraClave)
	tweets = client.search_recent_tweets(query=PalabraClave, max_results=100) #+ client.search_recent_tweets(query=PalabraClave, max_results=100))
	if tweets.data == None:
		return("No hay datos esta semana sobre la búsqueda")
	else:
		if os.path.exists('./busqueda.txt')==True:
			remove('./busqueda.txt')
		
		for tweet in tweets.data:
			f = open('./busqueda.json', 'a', encoding='utf-8')
			f.write(tweet.text + '\n')
			f.close
		return ("Los tweets están almacenados en busqueda.txt")


@app.route("/")
def home():
	return render_template("home.html")

@app.route("/Redecilla")
def RedecillaDelCamino():
	Resultado=BusquedaTweets("Redecilla Rollo de justicia")
	return(Resultado)

@app.route("/Castildelgado")
def Castildelgado():
	Resultado=BusquedaTweets("Castildelgado Palacio fortificado")
	return(Resultado)

@app.route("/Belorado")
def Belorado():
	Resultado=BusquedaTweets("Castillo de Belorado")
	return(Resultado)

@app.route("/Belorado2")
def Belorado2():
	Resultado=BusquedaTweets("Belorado")
	return(Resultado)