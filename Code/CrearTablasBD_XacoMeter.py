import psycopg2
import credencialesBD

creaTablaPatrimonio = ('''Create Table LISTADO_PATRIMONIOS(Patrimonio_Id BIGINT PRIMARY KEY, Patrimonio TEXT);'''
                        )

creaTablaTweets=('''Create Table TWEETS_PATRIMONIOS(Tweet_Id BIGINT,
                                         Patrimonio_Id BIGINT,
                                         Tweet_Texto TEXT,
                                         Tweet_CreatedAt DATE,
                                         Usuario_Username TEXT,
                                         Usuario_Verificado BOOLEAN,
                                         Lugar_GeoCoordenadas TEXT,
                                         Retweet_Count INT,
                                         PRIMARY KEY(Tweet_Id),
                                         FOREIGN KEY(Patrimonio_Id) REFERENCES LISTADO_PATRIMONIOS(Patrimonio_Id));'''
                                         
                )     

#Abre la conexion con la base de datos
conn = psycopg2.connect(host="localhost",database="XacoMeter",port=5432,user=credencialesBD.USUARIO,password=credencialesBD.CONTRASEÑA)
curs = conn.cursor()

#Carga las tablas con sus respectivas columnas
curs.execute(creaTablaPatrimonio)  
curs.execute(creaTablaTweets)

#Guarda los cambios y cierra la conexion con la base de datos
conn.commit()
curs.close()
conn.close()
