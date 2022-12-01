import psycopg2
import credencialesBD
import csv
from os import remove

def actualizaTablas(patrimonio):
    conn = psycopg2.connect(host="localhost",database="XacoMeter",port=5432,user=credencialesBD.USUARIO,password=credencialesBD.CONTRASEÑA)
    curs = conn.cursor()
    buscaIndex = ('''SELECT Patrimonio_Id FROM LISTADO_PATRIMONIOS WHERE Patrimonio = %s''')
    curs.execute(buscaIndex, [patrimonio])  
    conn.commit()
    curs.close()
    conn.close()            
def creaTablas(id, patrimonio):
    creaTablaPatrimonio = ('''CREATE TABLE IF NOT EXISTS LISTADO_PATRIMONIOS(Patrimonio_Id BIGINT PRIMARY KEY, Patrimonio TEXT);'''
                            )

    creaTablaTweets=('''CREATE TABLE IF NOT EXISTS TWEETS_PATRIMONIOS(
                                            Patrimonio_Id BIGINT,
                                            Tweet_Id BIGINT,
                                            User_Username TEXT,
                                            Lugar_GeoCoordenadas TEXT,
                                            Tweet_Lang TEXT,
                                            Tweet_Texto TEXT,
                                            User_Verified BOOLEAN,
                                            Retweet_Count INT,
                                            Like_Count INT,
                                            Reply_Count INT,
                                            Tweet_CreatedAt DATE, 
                                            PRIMARY KEY(Tweet_Id),
                                            FOREIGN KEY(Patrimonio_Id) REFERENCES LISTADO_PATRIMONIOS(Patrimonio_Id));'''
                                            
                    )   
    insertarTablaPatrimonio=('''INSERT INTO LISTADO_PATRIMONIOS(Patrimonio_Id, Patrimonio) 
                             VALUES (%s,%s) 
                             ON CONFLICT (Patrimonio_Id) DO UPDATE SET Patrimonio=(%s);''') 
    
    insertarTablaTweets = ('''INSERT INTO TWEETS_PATRIMONIOS
                           (Patrimonio_Id, Tweet_Id, Lugar_GeoCoordenadas, Tweet_Lang, Tweet_Texto, User_Username, User_Verified,
                          Retweet_Count, Like_Count, Reply_Count, Tweet_CreatedAt) 
                             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                             ON CONFLICT (Tweet_Id) DO NOTHING;''')

    #Abre la conexión con la base de datos
    conn = psycopg2.connect(host="localhost",database="XacoMeter",port=5432,user=credencialesBD.USUARIO,password=credencialesBD.CONTRASEÑA)
    curs = conn.cursor()

    #Carga las tablas con sus respectivas columnas
    curs.execute(creaTablaPatrimonio)  
    curs.execute(creaTablaTweets)
    
    #Inserta datos en las tablas
    variables = id, patrimonio, patrimonio
    curs.execute(insertarTablaPatrimonio, variables)
    
    #Definimos la ruta del archivo CSV
    CSVpath = "C:/tmp/temporal.csv"
    csvFile = open(CSVpath, "r", encoding='utf8')
    readCSV = csv.reader(csvFile, delimiter=',')
    for row in readCSV:
              rowVariables = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]
              curs.execute(insertarTablaTweets, rowVariables)
    
    csvFile.close()      
    remove("C:/tmp/temporal.csv")
    #Guarda los cambios y cierra la conexion con la base de datos
    conn.commit()
    curs.close()
    conn.close()
