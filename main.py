from flask import Flask, render_template, request, redirect, session, flash, url_for, make_response, send_file, get_flashed_messages
import os
from os import name, remove
import time
import Code.Destinos_XacoMeterII
import Code.Busqueda_XacoMeterII
import Code.CrearTablasBD_XacoMeterII
import Code.GraficosEstadisticas_XacoMeterII
import logging
import psycopg2
import psycopg2.extras
import datetime
from datetime import datetime,timedelta
from werkzeug.security import check_password_hash
import pandas as pd
import plotly.offline as plotly

app = Flask(__name__)
app.secret_key = 'Clave muy secreta sin revelacion'
app.config["SESSION_PERMANENT"] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta (minutes = 30)
app.config["SESSION_TYPE"] = "filesystem"
DEBUG = True
PORT = 5000

from dotenv import load_dotenv
load_dotenv()

@app.route("/")
def home():
    try:
        localidades=datosMapa()
        marcadores=[]
        ubicaciones=[]
        for i in localidades.index:
            marcadores.append([localidades.loc[i,'latitud'], localidades.loc[i,'longitud']])
            ubicaciones.append(localidades.loc[i,'denominacion'])  
        ubicacionesLista = [x.replace("'",' ') for x in ubicaciones]
        return render_template('home.html', marcadores = marcadores, ubicaciones=ubicacionesLista)
            
    except Exception as e:
        logging.error(f'{datetime.now()} - {e}')     
        return '<script>alert("Ha ocurrido un error en la aplicacion");</script>', 500
    
@app.route('/Login', methods = ['GET','POST'])
def Login():
    try:
        conn = psycopg2.connect(host=os.getenv("HOST"),database=os.getenv("DATABASE"),port=os.getenv("PUERTO"),user=os.getenv("USUARIO"),password=os.getenv("CLAVE"))
        curs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if ('usuario' and 'clave') in request.form:
            usuario = request.form.get ('usuario')
            clave = request.form.get ('clave')
            query = ('''SELECT * FROM usuarios WHERE username = %s''')
            curs.execute(query, [usuario])    
            datos = curs.fetchone()
            print(datos)
            if datos:
                clavebd = datos['password']
                if check_password_hash(clavebd, clave):
                    session['identificado'] = True
                    return redirect(url_for('AdministradorOpciones'))
            else:
                flash("Usuario o clave incorrectos. Vuelva a intentarlo.")
                return redirect(url_for('home'))
        curs.close()
        conn.close()
        return render_template('login.html')
            
    except Exception as e:
        logging.error(f'{datetime.now()} - {e}')     
        return redirect(url_for('home'))
    
@app.route('/Logout')
def Logout():
    try:
        session.pop('identificado',None)
        return redirect(url_for('home'))
            
    except Exception as e:
        logging.error(f'{datetime.now()} - {e}')     
        return redirect(url_for('home'))

@app.route('/Administrador', methods = ['GET','POST'])
def AdministradorOpciones():
    try:
        if 'identificado' in session:
            return render_template('administradorOpciones.html')
        else:
            return redirect (url_for('Login'))
                
    except Exception as e:
        logging.error(f'{datetime.now()} - {e}')     
        return redirect(url_for('home'))


@app.route('/Administrador/ActualizarBaseDeDatos', methods=['GET','POST'])
def AdministradorActualizar():
    try:
        if 'identificado' in session:
            if request.method=='GET':
                return render_template('admin_Actualizar.html')
            conn = psycopg2.connect(host=os.getenv("HOST"),database=os.getenv("DATABASE"),port=os.getenv("PUERTO"),user=os.getenv("USUARIO"),password=os.getenv("CLAVE"))
            total=0
            curs = conn.cursor()
            print("entro a recopilar datos 2do plano")
            ultimaFecha = Code.CrearTablasBD_XacoMeterII.ultimaFecha2(conn,curs)[0][0]
            ultimaFecha=datetime(ultimaFecha.year, ultimaFecha.month, ultimaFecha.day)
            fechaActual = datetime.now()
            fechaActual= fechaActual-timedelta(hours=1)
            cantDatos = int(request.form.get("datos"))
            tiempoCantidad = int(request.form.get("tiempoCantidad"))
            tiempoDia = int(request.form.get("tiempoDia"))
            Code.Destinos_XacoMeterII.buclePatrimonios(ultimaFecha,fechaActual,conn,curs,total, cantDatos, tiempoCantidad,tiempoDia)
            flash ("La base de datos ha sido actualizada")
            conn.commit()
            curs.close()
            conn.close()
            
            return redirect (url_for('home'))         
        else:
            return redirect (url_for('Login'))
        
    except Exception as e:
        flash ("La base de datos no ha sido actualizada")
        logging.error(f'{datetime.now()} - {e}')     
        return redirect(url_for('home'))
    

@app.route('/Administrador/CrearBaseDeDatos',methods = ['GET','POST'])
def AdministradorCrear():
    try:
        if 'identificado' in session:
            if request.method=='GET':
                return render_template('admin_Crear.html')
            conn = psycopg2.connect(host=os.getenv("HOST"),database=os.getenv("DATABASE"),port=os.getenv("PUERTO"),user=os.getenv("USUARIO"),password=os.getenv("CLAVE"))
            fechaElegida = request.form.get("fecha")
            cantDatos = int(request.form.get("datos"))
            tiempoCantidad = int(request.form.get("tiempoCantidad"))
            tiempoDia = int(request.form.get("tiempoDia"))
            partes=fechaElegida.split("-")
            fechaOrdenada="/".join(reversed(partes))
            fechaElegida=datetime.strptime(fechaOrdenada,"%d/%m/%Y")
            curs = conn.cursor()
            #Hay varias opciones: la base de datos tiene datos y se pueden recuperar o no existen datos
            primeraFecha=Code.CrearTablasBD_XacoMeterII.primeraFecha(conn,curs)[0][0]
            ultimaFecha=Code.CrearTablasBD_XacoMeterII.ultimaFecha2(conn,curs)[0][0]
            fechaActual = datetime.now()
            fechaActual= fechaActual-timedelta(hours=1)
            #Si no existen datos se crean de cero:

            if primeraFecha==None:
                index = 1
                total = 0
                diccionarioBusqueda = Code.Busqueda_XacoMeterII.palabrasClave()
                for x, y in diccionarioBusqueda.items():
                    total = Code.Destinos_XacoMeterII.OperacionesBD(index, x, y, fechaElegida,fechaActual, total, conn, curs, cantDatos, tiempoCantidad,tiempoDia)
                    index += 1
                    if total == cantDatos:
                        time.sleep(tiempoCantidad)
                        total=0
                conn.commit()
                curs.close()
                conn.close() 
            else:    
                primeraFecha=datetime(primeraFecha.year, primeraFecha.month, primeraFecha.day)
                ultimaFecha=datetime(ultimaFecha.year, ultimaFecha.month, ultimaFecha.day)
                total = 0
            
                #Si existen datos, para aumentar el rendimiento de la web y no tener que hacer tantas consultas a la API se reutilizan datos de la BBDD
                if primeraFecha<=fechaElegida<=ultimaFecha:
                    #Destinos_XacoMeterII.buclePatrimonios(ultimaFecha,fechaActual,conn,curs,total, cantDatos, tiempoCantidad,tiempoDia)
                    Code.CrearTablasBD_XacoMeterII.borradoTablas(primeraFecha,fechaElegida,conn,curs)
                    Code.CrearTablasBD_XacoMeterII.quitaBorradoTablas(fechaElegida,fechaActual,conn,curs)
                    conn.commit()
                    curs.close()
                    conn.close()   
                    
                elif fechaElegida<primeraFecha:
                    total=Code.Destinos_XacoMeterII.buclePatrimonios(fechaElegida,primeraFecha,conn,curs,total, cantDatos, tiempoCantidad,tiempoDia)
                    conn.commit()
                    Code.Destinos_XacoMeterII.buclePatrimonios(ultimaFecha,fechaActual,conn,curs,total, cantDatos, tiempoCantidad,tiempoDia)
                    Code.CrearTablasBD_XacoMeterII.quitaBorradoTablas(fechaElegida,fechaActual,conn,curs)
                    conn.commit()
                    curs.close()
                    conn.close()

                else:
                    Code.CrearTablasBD_XacoMeterII.borradoTablas(primeraFecha,fechaElegida,conn,curs)
                    Code.Destinos_XacoMeterII.buclePatrimonios(ultimaFecha,fechaActual,conn,curs,total, cantDatos, tiempoCantidad,tiempoDia)
                    Code.CrearTablasBD_XacoMeterII.borradoTablas(ultimaFecha,fechaElegida,conn,curs)
                    Code.CrearTablasBD_XacoMeterII.quitaBorradoTablas(fechaElegida,fechaActual,conn,curs)
                    conn.commit()
                    curs.close()
                    conn.close()
            flash('La base de datos ha sido creada correctamente')
            return redirect(url_for('AdministradorOpciones'))

        else:
            return redirect (url_for('Login'))
        
    except Exception as e:
        logging.error(f'{datetime.now()} - {e}')     
        return redirect(url_for('home'))

@app.route('/estadisticasTemporales/<string:patrimonio>')    
def estadisticasTemporales(patrimonio):
    try:
        conn = psycopg2.connect(host=os.getenv("HOST"),database=os.getenv("DATABASE"),port=os.getenv("PUERTO"),user=os.getenv("USUARIO"),password=os.getenv("CLAVE"))
        curs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        patrimonio = str(patrimonio.replace('+',' '))
        primeraFecha = request.args.get('fechaInicio')
        ultimaFecha = request.args.get('fechaFin')
        primeraFechaBD=Code.CrearTablasBD_XacoMeterII.primeraFechaEstadisticas(patrimonio,conn,curs)['date']
        ultimaFechaBD=Code.CrearTablasBD_XacoMeterII.ultimaFechaEstadisticas(patrimonio,conn,curs)['date']
        if primeraFecha==None or len(primeraFecha)==None:
            primeraFecha=primeraFechaBD
        if ultimaFecha==None or len(ultimaFecha)==None:
            ultimaFecha=ultimaFechaBD
        print(primeraFecha)
        print(ultimaFecha)
        diccionario=Code.CrearTablasBD_XacoMeterII.sacaDatosPatrimonio(conn, curs, primeraFecha, ultimaFecha, patrimonio)
        total=Code.CrearTablasBD_XacoMeterII.cuentaFilasTotales(conn, curs)
        print(total)
        date_range = pd.date_range(primeraFecha, ultimaFecha)
        date_range_df = pd.DataFrame({'Fechas': date_range})
        titulos = ['Fechas', 'Retweet', 'Like', 'Reply', 'filas']
        df = pd.DataFrame(diccionario, columns=titulos)
        df['Fechas'] = pd.to_datetime(df['Fechas'])
        merged_data = pd.merge(df, date_range_df, on='Fechas', how='right')
        merged_data = merged_data.fillna(0)
        print(merged_data)
        graficoLineas=Code.GraficosEstadisticas_XacoMeterII.graficoLineas(merged_data,patrimonio)
        print('ggg')
        graficoCircular=Code.GraficosEstadisticas_XacoMeterII.graficoCircular(merged_data,total,patrimonio)
        print('hhh')
        graficoBarras=Code.GraficosEstadisticas_XacoMeterII.graficoBarras(merged_data,patrimonio)
        return render_template('serieTemporal.html', nombre=patrimonio, graficoLineas=graficoLineas, graficoCircular=graficoCircular, graficoBarras=graficoBarras, fechaInicio=primeraFecha, fechaFin=ultimaFecha, primeraBD=primeraFechaBD, ultimaBD=ultimaFechaBD)
    
    except Exception as e:
        logging.error(f'{datetime.now()} - {e}')     
        return redirect(url_for('home'))

@app.route('/descargar_csv/<string:patrimonio>/<string:primeraFecha>/<string:ultimaFecha>')
def descargar_csv(patrimonio, primeraFecha, ultimaFecha):
    try:
        conn = psycopg2.connect(host=os.getenv("HOST"),database=os.getenv("DATABASE"),port=os.getenv("PUERTO"),user=os.getenv("USUARIO"),password=os.getenv("CLAVE"))
        curs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        diccionario=Code.CrearTablasBD_XacoMeterII.sacaDatosPatrimonioDescargar(conn, curs, primeraFecha, ultimaFecha, patrimonio)
        titulos = ['Patrimonio_Nombre','Patrimonio_Id', 'Tweet_Id', 'Lugar_Id', 'Tweet_Idioma', 'Tweet_Texto', 
                    'Usuario_Username', 'Usuario_Verificado',
                    'Retweet_Numero', 'Like_Numero', 'Reply_Numero', 'Tweet_FechaCreación', 'Borrado']
        df = pd.DataFrame(diccionario, columns=titulos)
        df['Fechas'] = pd.to_datetime(df['Tweet_FechaCreación'])
        response = make_response(df.to_csv(index=False, encoding='utf-8'))
        response.headers["Content-Disposition"] = "attachment; filename=patrimonio.csv"
        response.headers["Content-Type"] = "text/csv"
        return response
    except Exception as e:
        logging.error(f'{datetime.now()} - {e}')
        return redirect(url_for('home'))
        
@app.route('/logErrores')
def LogErrores():
    try:
        if 'identificado' in session:
            return send_file('errores.log', attachment_file='errores.log')
        else:
            return redirect(url_for('home'))
    except:
        return redirect(url_for('home'))

class ExceptionFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.WARNING
    
error_filter = ExceptionFilter()
file_handler = logging.FileHandler(filename='errores.log')
file_handler.addFilter(error_filter)
logging.getLogger().addHandler(file_handler)

@app.errorhandler(Exception)
def handle_generic_error(error):
    logging.error(f'{datetime.now()} - APP ERROR - {error}')
    return '<script>alert("Ha ocurrido un error en la aplicacion");</script>', 500

def datosMapa():
    ruta_archivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'inventario_01.csv')
    locations=pd.read_csv(ruta_archivo,sep=';',index_col=0)   
    return locations


if __name__ == '__main__':
    app.run(port = PORT, debug = DEBUG)
