from os import remove
from datetime import date
import dateutil
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

def primeraFecha(conn, curs):
    buscaFecha = ('''SELECT MIN(Tweet_CreatedAt) as date FROM TWEETS_PATRIMONIOS''')
    curs.execute(buscaFecha) 
    primerafecha=curs.fetchone() 
    return primerafecha

def ultimaFecha(conn, curs):
    buscaFecha = ('''SELECT MAX(Tweet_CreatedAt) as date FROM TWEETS_PATRIMONIOS''')
    curs.execute(buscaFecha) 
    ultimafecha=curs.fetchone() 
    return ultimafecha

def primeraFechaEstadisticas(patrimonio, conn, curs):
    buscaFecha = ('''SELECT MIN(Tweet_CreatedAt) as date
                  FROM TWEETS_PATRIMONIOS 
                  WHERE TWEETS_PATRIMONIOS.Borrado=False
                ''')
    curs.execute(buscaFecha, [patrimonio]) 
    fecha=curs.fetchone() 
    return fecha


def ultimaFechaEstadisticas(patrimonio, conn, curs):
    buscaFecha = ('''SELECT MAX(Tweet_CreatedAt) as date
                  FROM TWEETS_PATRIMONIOS 
                  WHERE TWEETS_PATRIMONIOS.Borrado=False
                ''')
    curs.execute(buscaFecha, [patrimonio]) 
    fecha=curs.fetchone() 
    return fecha

def sacaDatosPatrimonio(conn, curs, fechaInicio, fechaFin, patrimonio):
    sacaDatos =('''SELECT TWEETS_PATRIMONIOS.Tweet_CreatedAt as date, SUM(TWEETS_PATRIMONIOS.Retweet_Count) as rt, SUM(TWEETS_PATRIMONIOS.Like_Count) as like, SUM(TWEETS_PATRIMONIOS.Reply_Count) as rp, COUNT(*) as filas
                FROM TWEETS_PATRIMONIOS
                WHERE TWEETS_PATRIMONIOS.Patrimonio_Id = (SELECT IDPatrimonio FROM LISTADO_PATRIMONIOS WHERE Patrimonio = %s) 
                AND (TWEETS_PATRIMONIOS.Tweet_CreatedAt >= %s AND TWEETS_PATRIMONIOS.Tweet_CreatedAt <= %s)
                AND TWEETS_PATRIMONIOS.Borrado = ('False')
                GROUP BY TWEETS_PATRIMONIOS.Tweet_CreatedAt''')
    variables = patrimonio, fechaInicio, fechaFin
    curs.execute(sacaDatos, variables)
    registros = curs.fetchall()
    return registros

def sacaDatosGenerales(conn, curs, fechaInicio, fechaFin):
    sacaDatos =('''SELECT Listado_Patrimonios.IDPatrimonio as idPatrimonio, Listado_Patrimonios.Patrimonio as patrimonio, COALESCE(COUNT(tweets_patrimonios.Patrimonio_Id), 0) as filas
                FROM Listado_Patrimonios
                LEFT JOIN TWEETS_PATRIMONIOS ON Listado_Patrimonios.IDPatrimonio=TWEETS_PATRIMONIOS.Patrimonio_Id
                AND TWEETS_PATRIMONIOS.Borrado = 'FALSE'
                AND (TWEETS_PATRIMONIOS.Tweet_CreatedAt >= %s AND TWEETS_PATRIMONIOS.Tweet_CreatedAt <= %s)
                GROUP BY Listado_Patrimonios.IDPatrimonio, Listado_Patrimonios.Patrimonio''')
    variables = fechaInicio, fechaFin
    curs.execute(sacaDatos, variables)
    registros = curs.fetchall()
    return registros

def sacaDatosPatrimonioDescargar(conn, curs, fechaInicio, fechaFin, patrimonio):
    sacaDatos =('''SELECT LISTADO_PATRIMONIOS.Patrimonio, Patrimonio_Id, Tweet_Id, Lugar_GeoCoordenadas, Tweet_Lang, Tweet_Texto, 
                    User_Username, User_Verified,
                    Retweet_Count, Like_Count, Reply_Count, Tweet_CreatedAt, Borrado
                FROM TWEETS_PATRIMONIOS INNER JOIN LISTADO_PATRIMONIOS 
                ON LISTADO_PATRIMONIOS.IDPatrimonio=TWEETS_PATRIMONIOS.Patrimonio_Id
                WHERE LISTADO_PATRIMONIOS.Patrimonio = %s
                AND (TWEETS_PATRIMONIOS.Tweet_CreatedAt >= %s AND TWEETS_PATRIMONIOS.Tweet_CreatedAt <= %s) 
                AND TWEETS_PATRIMONIOS.Borrado = ('False')
                ''')
    variables = patrimonio, fechaInicio, fechaFin
    curs.execute(sacaDatos, variables)
    registros = curs.fetchall()
    return registros

def cuentaFilasTotales(conn, curs):
    cuentaFilasTotales =('''SELECT COUNT(*) FROM TWEETS_PATRIMONIOS
                ''')
    curs.execute(cuentaFilasTotales)
    registros = curs.fetchone()
    return registros

def cuentaDatos(conn, curs, fecha, patrimonio):
    cuentaTweets =('''SELECT COUNT (*) FROM TWEETS_PATRIMONIOS INNER JOIN LISTADO_PATRIMONIOS 
                   ON LISTADO_PATRIMONIOS.IDPatrimonio=TWEETS_PATRIMONIOS.Patrimonio_Id
                   WHERE LISTADO_PATRIMONIOS.Patrimonio = %s AND TWEETS_PATRIMONIOS.Tweet_CreatedAt = %s 
                   AND TWEETS_PATRIMONIOS.Borrado=('False')''')
    variables = patrimonio, fecha
    curs.execute(cuentaTweets, variables)
    numeroDatos = curs.fetchone()
    return numeroDatos

def cuentaFilas(conn,curs,fechaIni, fechaFin):
    cuentaFilas=('''SELECT COUNT(*) FROM TWEETS_PATRIMONIOS 
                 WHERE Tweet_CreatedAt BETWEEN %s AND %s AND TWEETS_PATRIMONIOS.Borrado=('False')''')
    variables = fechaIni, fechaFin
    curs.execute(cuentaFilas, variables)
    numeroDatos = curs.fetchone()
    return numeroDatos


def insertarDatos(PatrimonioId, diccionarioTweets, patrimonio, conn, curs):
    if ('data' in diccionarioTweets)  :
        for tweet, usuario in zip (diccionarioTweets['data'], diccionarioTweets['includes']['users']):
            text = str(tweet['text'])
            tweet_id = int(tweet['id'])
            username = str(usuario['username'])
            createdAt = dateutil.parser.parse(tweet['created_at'])
            if ('geo' in tweet):   
                geo = str(tweet['geo'])
            else:
                geo = "No hay geolocalización"
            lang = str(tweet['lang'])
            text = str(tweet['text'])
            verified = bool(usuario['verified'])
            retweet_count = int(tweet['public_metrics']['retweet_count'])
            like_count = int(tweet['public_metrics']['like_count'])
            reply_count = int(tweet['public_metrics']['reply_count'])
            if not text.startswith("RT"):
                insertarTablaPatrimonio=('''INSERT INTO LISTADO_PATRIMONIOS(IDPatrimonio, Patrimonio) 
                             VALUES (%s,%s) 
                             ON CONFLICT (IDPatrimonio) DO UPDATE SET Patrimonio=(%s);''')
                variablesPatrimonio = PatrimonioId, patrimonio, patrimonio
                curs.execute(insertarTablaPatrimonio, variablesPatrimonio)
     
                insertarTablaTweets = ('''INSERT INTO TWEETS_PATRIMONIOS
                           (Patrimonio_Id, Tweet_Id, Lugar_GeoCoordenadas, Tweet_Lang, Tweet_Texto, User_Username, User_Verified,
                          Retweet_Count, Like_Count, Reply_Count, Tweet_CreatedAt, Borrado) 
                             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'False') 
                             ON CONFLICT (Tweet_Id) DO UPDATE SET Borrado=('False');''')
                variablesTweets = PatrimonioId, tweet_id, geo, lang, text, username, verified, retweet_count, like_count,reply_count, createdAt
                curs.execute(insertarTablaTweets, variablesTweets)
    
