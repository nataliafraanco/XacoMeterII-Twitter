import csv
from os import remove
from datetime import date

def borradoTablas(primeraFecha,ultimaFecha,conn,curs):
    primeraFecha=primeraFecha.date()
    print(primeraFecha)
    ultimaFecha=ultimaFecha.date()
    #Borra las tablas de la base de datos
    borrado = ('''UPDATE TWEETS_PATRIMONIOS SET Borrado = ('True') WHERE (Tweet_CreatedAt>=%s AND Tweet_CreatedAt<%s)''')
    fechas = primeraFecha,ultimaFecha
    curs.execute(borrado,fechas) 
    #Guarda los cambios y cierra la conexion con la base de datos
    
def quitaBorradoTablas(primeraFecha,ultimaFecha,conn,curs):
    primeraFecha=primeraFecha.date()
    print(primeraFecha)
    ultimaFecha=ultimaFecha.date()
    #Borra las tablas de la base de datos
    borrado = ('''UPDATE TWEETS_PATRIMONIOS SET Borrado = ('False') WHERE (Tweet_CreatedAt>=%s AND Tweet_CreatedAt<%s)''')
    fechas = primeraFecha,ultimaFecha
    curs.execute(borrado,fechas)     
    
def actualizaTablas(patrimonio, conn, curs):
    buscaIndex = ('''SELECT IDPatrimonio FROM LISTADO_PATRIMONIOS WHERE Patrimonio LIKE %s ''')
    curs.execute(buscaIndex, [patrimonio])  
    index=curs.fetchall() 
    return index 

def ultimaFecha(index, conn, curs):
    #Pensar qué hacer si no hay bd
    buscaFecha = ('''SELECT MAX(Tweet_CreatedAt) FROM TWEETS_PATRIMONIOS WHERE Patrimonio_Id = %s''')
    curs.execute(buscaFecha, [index]) 
    fecha=curs.fetchall() 
    return fecha

def primeraFecha(conn, curs):
    #Pensar qué hacer si no hay bd
    buscaFecha = ('''SELECT MIN(Tweet_CreatedAt) FROM TWEETS_PATRIMONIOS''')
    curs.execute(buscaFecha) 
    primerafecha=curs.fetchall() 
    return primerafecha

def ultimaFecha2(conn, curs):
    #Pensar qué hacer si no hay bd
    buscaFecha = ('''SELECT MAX(Tweet_CreatedAt) FROM TWEETS_PATRIMONIOS''')
    curs.execute(buscaFecha) 
    ultimafecha=curs.fetchall() 
    return ultimafecha

def insertaDatos(id, patrimonio,conn,curs):

    insertarTablaPatrimonio=('''INSERT INTO LISTADO_PATRIMONIOS(IDPatrimonio, Patrimonio) 
                             VALUES (%s,%s) 
                             ON CONFLICT (IDPatrimonio) DO UPDATE SET Patrimonio=(%s);''') 
    
    insertarTablaTweets = ('''INSERT INTO TWEETS_PATRIMONIOS
                           (Patrimonio_Id, Tweet_Id, Lugar_GeoCoordenadas, Tweet_Lang, Tweet_Texto, User_Username, User_Verified,
                          Retweet_Count, Like_Count, Reply_Count, Tweet_CreatedAt, Borrado) 
                             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'False') 
                             ON CONFLICT (Tweet_Id) DO UPDATE SET Borrado=('False');''')
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
    

    
    
