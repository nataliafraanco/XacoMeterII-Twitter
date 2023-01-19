from flask import Flask, render_template, request, redirect, session, flash, url_for, make_response, send_file, get_flashed_messages
import os
from os import name
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

from subprocess import Popen

app = Flask(__name__)
app.secret_key = 'Clave muy secreta sin revelacion'
app.config["SESSION_PERMANENT"] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta (minutes = 30)
app.config["SESSION_TYPE"] = "filesystem"
DEBUG = False
PORT = 5000
''' 
from dotenv import load_dotenv
load_dotenv()
''' 
@app.route("/")
def home():
    localidades=datosMapa()
    marcadores=[]
    ubicaciones=[]
    for i in localidades.index:
        marcadores.append([localidades.loc[i,'latitud'], localidades.loc[i,'longitud']])
        ubicaciones.append(localidades.loc[i,'denominacion'])  
    ubicacionesLista = [x.replace("'",' ') for x in ubicaciones]
    return render_template('home.html', marcadores = marcadores, ubicaciones=ubicacionesLista)
''' 
@app.route('/Login', methods = ['GET','POST'])
def Login():
    conn = psycopg2.connect(host=os.getenv("HOST"),database=os.getenv("DATABASE"),port=os.getenv("PUERTO"),user=os.getenv("USUARIO"),password=os.getenv("CLAVE"))
    curs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if ('usuario' and 'clave') in request.form:
        usuario = request.form.get ('usuario')
        clave = request.form.get ('clave')
        query = ('''SELECT * FROM usuarios WHERE username = %s''')
        curs.execute(query, [usuario])    
        datos = curs.fetchone()
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
   
@app.route('/Logout')
def Logout():
    session.pop('identificado',None)
    return redirect(url_for('home'))

@app.route('/Administrador', methods = ['GET','POST'])
def AdministradorOpciones():
    if 'identificado' in session:
        return render_template('administradorOpciones.html')
    else:
        return redirect (url_for('Login'))

@app.route('/Administrador/ActualizarBaseDeDatos')
def AdministradorActualizarVista():
    return render_template('admin_Actualizar.html')

@app.route('/Administrador/ActualizarBaseDeDatos', methods=['POST'])
def AdministradorActualizar():
    if 'identificado' in session:
        conn = psycopg2.connect(host=os.getenv("HOST"),database=os.getenv("DATABASE"),port=os.getenv("PUERTO"),user=os.getenv("USUARIO"),password=os.getenv("CLAVE"))
        total=0
        curs = conn.cursor()
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
        return redirect(url_for('AdministradorOpciones'))
    else:
        return redirect (url_for('Login'))

@app.route('/Administrador/CrearBaseDeDatos')
def eligeFecha():
    return render_template('admin_Crear.html')

@app.route('/Administrador/CrearBaseDeDatos',methods = ['POST'])
def AdministradorCrear():
    if 'identificado' in session:
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
            if primeraFecha<=fechaElegida<ultimaFecha:
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


@app.route('/estadisticasTemporales/<string:patrimonio>')    
def estadisticasTemporales(patrimonio):
    try:
        conn = psycopg2.connect(host=os.getenv("HOST"),database=os.getenv("DATABASE"),port=os.getenv("PUERTO"),user=os.getenv("USUARIO"),password=os.getenv("CLAVE"))
        curs = conn.cursor()
        primeraFecha = request.args.get('fechaInicio')
        ultimaFecha = request.args.get('fechaFin')
        if primeraFecha==None or len(primeraFecha)==None:
            primeraFecha=Code.CrearTablasBD_XacoMeterII.primeraFecha(conn,curs)[0][0]
        else:
            primeraFecha = datetime.strptime(primeraFecha, "%Y-%m-%d")
        if ultimaFecha==None or len(ultimaFecha)==None:
            ultimaFecha=Code.CrearTablasBD_XacoMeterII.ultimaFecha2(conn,curs)[0][0]
        else:
            ultimaFecha = datetime.strptime(ultimaFecha, "%Y-%m-%d")
        graficoTemporal=Code.GraficosEstadisticas_XacoMeterII.graficoTemporal(patrimonio, primeraFecha, ultimaFecha, conn, curs)
        graficoCircular=Code.GraficosEstadisticas_XacoMeterII.graficoCircularTotal(patrimonio, primeraFecha, ultimaFecha, conn, curs)
        graficoMetricasPublicas=Code.GraficosEstadisticas_XacoMeterII.graficoMetricasPublicas(patrimonio, primeraFecha, ultimaFecha, conn, curs)
        html = render_template('serieTemporal.html', graficoTemporal=graficoTemporal, graficoCircular=graficoCircular, graficoMetricasPublicas=graficoMetricasPublicas)
        with open('temp.html', 'w') as f:
            f.write(html)
        p = Popen(['C:\\tmp\\wkhtmltopdf\\bin\\wkhtmltopdf.exe','--enable-local-file-access','--no-background','temp.html', 'outputPDF.pdf'])
        p.wait()
        os.remove('temp.html')
        return render_template('serieTemporal.html', graficoTemporal=graficoTemporal, graficoCircular=graficoCircular, graficoMetricasPublicas=graficoMetricasPublicas)
    except Exception as e:
        flash('Ha ocurrido una excepcion mientras se intentaban realizar las estadísticas')
        logging.error(f'{datetime.now()} - {e}')     
        return redirect(url_for('home'))
    
@app.route('/logErrores')
def LogErrores():
    try:
        return send_file('errores.log', attachment_file='errores.log')
    except:
        flash('Ha ocurrido una excepcion mientras se intentaba descargar el archivo')
        return redirect(request.referrer)
'''      
@app.route('/descargaPDF', methods=['POST'])
def descarga():
    with open('outputPDF.pdf', 'rb') as f:
        pdf = f.read()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=estadisticasTemporales.pdf'
    return response
'''
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
'''
def datosMapa():
    locations=pd.read_csv('.\data\inventario_01.csv',sep=';',index_col=0)   
    return locations


if __name__ == '__main__':
    app.run(port = PORT, debug = DEBUG)
