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

def cuentaDatos(conn, curs, fecha, patrimonio):
    cuentaTweets =('''SELECT COUNT (*) FROM TWEETS_PATRIMONIOS INNER JOIN LISTADO_PATRIMONIOS 
                   ON LISTADO_PATRIMONIOS.IDPatrimonio=TWEETS_PATRIMONIOS.Patrimonio_Id
                   WHERE LISTADO_PATRIMONIOS.Patrimonio = %s AND TWEETS_PATRIMONIOS.Tweet_CreatedAt = %s''')
    variables = patrimonio, fecha
    curs.execute(cuentaTweets, variables)
    numeroDatos = curs.fetchone()
    return numeroDatos

def cuentaFilas(conn,curs,fechaIni, fechaFin):
    cuentaFilas=('''SELECT COUNT(*) FROM TWEETS_PATRIMONIOS 
                 WHERE Tweet_CreatedAt BETWEEN %s AND %s''')
    variables = fechaIni, fechaFin
    curs.execute(cuentaFilas, variables)
    numeroDatos = curs.fetchone()
    return numeroDatos



def cuentaLikes(conn,curs,fecha, patrimonio):
    cuentaLikes=('''SELECT Like_Count FROM TWEETS_PATRIMONIOS INNER JOIN LISTADO_PATRIMONIOS 
                    ON LISTADO_PATRIMONIOS.IDPatrimonio=TWEETS_PATRIMONIOS.Patrimonio_Id
                    WHERE TWEETS_PATRIMONIOS.Tweet_Texto NOT LIKE %s AND LISTADO_PATRIMONIOS.Patrimonio = %s AND
                    TWEETS_PATRIMONIOS.Tweet_CreatedAt = %s''')
    variables = 'RT', patrimonio, fecha
    curs.execute(cuentaLikes, variables)
    numeroDatos = curs.fetchall()
    soloValor=[]
    if numeroDatos==None:
        numeroDatos=0
        return numeroDatos
    else:
        for dato in numeroDatos:
            soloValor.append(dato[0])
        return sum(soloValor)

def cuentaReply(conn,curs,fecha, patrimonio):
    cuentaReply=('''SELECT Reply_Count FROM TWEETS_PATRIMONIOS INNER JOIN LISTADO_PATRIMONIOS 
                    ON LISTADO_PATRIMONIOS.IDPatrimonio=TWEETS_PATRIMONIOS.Patrimonio_Id
                    WHERE TWEETS_PATRIMONIOS.Tweet_Texto NOT LIKE %s AND LISTADO_PATRIMONIOS.Patrimonio = %s AND
                    TWEETS_PATRIMONIOS.Tweet_CreatedAt = %s''')
    variables = 'RT%', patrimonio, fecha 
    curs.execute(cuentaReply, variables)
    numeroDatos = curs.fetchall()
    soloValor=[]
    if numeroDatos==None:
        numeroDatos=0
        return numeroDatos
    else:
        for dato in numeroDatos:
            soloValor.append(dato[0])
        return sum(soloValor)

def cuentaRetweet(conn,curs,fecha, patrimonio):
    cuentaRetweet=('''SELECT Retweet_Count FROM TWEETS_PATRIMONIOS INNER JOIN LISTADO_PATRIMONIOS 
                    ON LISTADO_PATRIMONIOS.IDPatrimonio=TWEETS_PATRIMONIOS.Patrimonio_Id
                    WHERE TWEETS_PATRIMONIOS.Tweet_Texto NOT LIKE %s AND LISTADO_PATRIMONIOS.Patrimonio = %s AND
                    TWEETS_PATRIMONIOS.Tweet_CreatedAt = %s''')
    variables = 'RT%', patrimonio, fecha
    curs.execute(cuentaRetweet, variables)
    numeroDatos = curs.fetchall()
    soloValor=[]
    if numeroDatos==None:
        numeroDatos=0
        return numeroDatos
    else:
        for dato in numeroDatos:
            soloValor.append(dato[0])
        return sum(soloValor)
        

def cuentaFilasPatrimonio(conn,curs,fechaIni, fechaFin, patrimonio):
    cuentaFilas=('''SELECT COUNT(*) FROM TWEETS_PATRIMONIOS INNER JOIN LISTADO_PATRIMONIOS 
                    ON LISTADO_PATRIMONIOS.IDPatrimonio=TWEETS_PATRIMONIOS.Patrimonio_Id
                    WHERE LISTADO_PATRIMONIOS.Patrimonio = %s AND
                    TWEETS_PATRIMONIOS.Tweet_CreatedAt BETWEEN %s AND %s ''')
    variables = patrimonio, fechaIni, fechaFin 
    curs.execute(cuentaFilas, variables)
    numeroDatos = curs.fetchone()
    return numeroDatos

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
    

    
    
