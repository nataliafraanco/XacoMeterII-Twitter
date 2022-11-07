import psycopg2
import credencialesBD


def insertar_TablaPatrimonio (id_Patrimonio, nombre_Patrimonio):
    
    insertaTablaPatrimonio = ('''INSERT INTO LISTADO_PATRIMONIOS (patrimonio_id, patrimonio) VALUES (1, 'Catedral de Burgos');''' #.format(id_Patrimonio, nombre_Patrimonio)
                        )


    conn = psycopg2.connect(host="localhost",database="XacoMeter",port=5432,user=credencialesBD.USUARIO,password=credencialesBD.CONTRASEÑA)
    curs = conn.cursor()

    #Carga las tablas con sus respectivas columnas
    curs.execute(insertaTablaPatrimonio)  


    #Guarda los cambios y cierra la conexion con la base de datos
    conn.commit()
    curs.close()    
    conn.close()
