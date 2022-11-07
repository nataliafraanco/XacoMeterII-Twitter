from pymongo import MongoClient

MongoDBClient = MongoClient("mongodb://")

#Si la base de datos no existe la crea:
db = MongoDBClient("mongodb+srv://Natalia:kittylonga12@atlascluster.izdcljf.mongodb.net/?retryWrites=true&w=majority")
tweets = db("tweets_patrimonios")