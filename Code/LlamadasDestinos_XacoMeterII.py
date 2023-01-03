from os import name
import time
import Destinos_XacoMeterII
import Busqueda_XacoMeterII
import CrearTablasBD_XacoMeterII
import GraficosEstadisticas_XacoMeterII
from flask import Flask, render_template, request, redirect, session, flash, url_for
import psycopg2
import psycopg2.extras
import credencialesBD
import datetime
from datetime import datetime,timedelta
from werkzeug.security import check_password_hash
import folium
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import csv
import pandas as pd
import itertools
app = Flask(__name__)
app.secret_key = 'Secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta (minutes = 30)
#app.config['GOOGLEMAPS_KEY'] = credencialesAPIGoogle.claveAPIGoogle
DEBUG = False
PORT = 5000
#GoogleMaps(app)

@app.route("/")
def home():
    localidades=datosMapa()
    mapaLocalidades = folium.Map(
        zoom_start=8,
        # Mapa centrado en Sahagun
        location=[42.37014,-5.030849],
          
    )

    marcadores=[]
    ubicaciones=[]
    for i in localidades.index:
        
        location=[localidades.loc[i,'latitud'], localidades.loc[i,'longitud']]
        ubicacion=localidades.loc[i,'denominacion']
        #marcador = folium.Marker(location, popup = cajaInformacion(localidades.loc[i,'denominacion']))
        marcadores.append(location)
        ubicaciones.append(ubicacion)
        print(ubicaciones[0])       
       
    return render_template('home.html', marcadores = marcadores, ubicaciones=ubicaciones, map=mapaLocalidades,localidades=localidades)

@app.route("/Burgos",methods=['GET','POST'])
def Burgos():
    return render_template('Burgos.html')


@app.route('/Login', methods = ['GET','POST'])
def Login():
    conn = psycopg2.connect(host="localhost",database="XacoMeter",port=5432,user=credencialesBD.USUARIO,password=credencialesBD.CONTRASEÑA)
    curs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if ('usuario' and 'contraseña') in request.form:
        usuario = request.form.get ('usuario')
        print(usuario)
        contraseña = request.form.get ('contraseña')
        query = ('''SELECT * FROM usuarios WHERE username = %s''')
        curs.execute(query, [usuario])    
        datos = curs.fetchone()
        if datos:
            contraseñabd = datos['password']
            if check_password_hash(contraseñabd, contraseña):
                session['identificado'] = True
                return redirect(url_for('AdministradorOpciones'))
        else:
            flash("Usuario o contraseña incorrectos. Vuelva a intentarlo.")
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
        conn = psycopg2.connect(host="localhost",database="XacoMeter",port=5432,user=credencialesBD.USUARIO,password=credencialesBD.CONTRASEÑA)
        total=0
        curs = conn.cursor()
        ultimaFecha = CrearTablasBD_XacoMeterII.ultimaFecha2(conn,curs)[0][0]
        ultimaFecha=datetime(ultimaFecha.year, ultimaFecha.month, ultimaFecha.day)
        fechaActual = datetime.now()
        fechaActual= fechaActual-timedelta(hours=1)
        cantDatos = int(request.form.get("datos"))
        tiempoCantidad = int(request.form.get("tiempoCantidad"))
        tiempoDia = int(request.form.get("tiempoDia"))
        Destinos_XacoMeterII.buclePatrimonios(ultimaFecha,fechaActual,conn,curs,total, cantDatos, tiempoCantidad,tiempoDia)
        flash ("La base de datos ha sido actualizada")
        conn.commit()
        curs.close()
        conn.close()
        return redirect('/home')
    else:
        return redirect (url_for('Login'))

@app.route('/Administrador/CrearBaseDeDatos')
def eligeFecha():
    return render_template('admin_Crear.html')

@app.route('/Administrador/CrearBaseDeDatos',methods = ['POST'])
def AdministradorCrear():
    if 'identificado' in session:
        conn = psycopg2.connect(host="localhost",database="XacoMeter",port=5432,user=credencialesBD.USUARIO,password=credencialesBD.CONTRASEÑA)
        fechaElegida = request.form.get("fecha")
        cantDatos = int(request.form.get("datos"))
        tiempoCantidad = int(request.form.get("tiempoCantidad"))
        tiempoDia = int(request.form.get("tiempoDia"))
        partes=fechaElegida.split("-")
        fechaOrdenada="/".join(reversed(partes))
        fechaElegida=datetime.strptime(fechaOrdenada,"%d/%m/%Y")
        curs = conn.cursor()
        #Hay varias opciones: la base de datos tiene datos y se pueden recuperar o no existen datos
        primeraFecha=CrearTablasBD_XacoMeterII.primeraFecha(conn,curs)[0][0]
        ultimaFecha=CrearTablasBD_XacoMeterII.ultimaFecha2(conn,curs)[0][0]
        fechaActual = datetime.now()
        fechaActual= fechaActual-timedelta(hours=1)
        #Si no existen datos se crean de cero:
        if primeraFecha==None:
            index = 1
            total = 0
            diccionarioBusqueda = Busqueda_XacoMeterII.palabrasClave()
            for x, y in diccionarioBusqueda.items():
                total = Destinos_XacoMeterII.OperacionesBD(index, x, y, fechaElegida,fechaActual, total, conn, curs, cantDatos, tiempoCantidad,tiempoDia)
                index += 1
                if total == cantDatos:
                    time.sleep(tiempoCantidad)
                    total=0
                print (total)
            conn.commit()
            curs.close()
            conn.close() 
        else:    
            primeraFecha=datetime(primeraFecha.year, primeraFecha.month, primeraFecha.day)
            ultimaFecha=datetime(ultimaFecha.year, ultimaFecha.month, ultimaFecha.day)
            total = 0
            print("---------")
            print(cantDatos)
            print(tiempoCantidad)
            print(tiempoDia)
            print(ultimaFecha)
            print(fechaActual)
        
            #Si existen datos, para aumentar el rendimiento de la web y no tener que hacer tantas consultas a la API se reutilizan datos de la BBDD
            if primeraFecha<=fechaElegida<ultimaFecha:
                #Destinos_XacoMeterII.buclePatrimonios(ultimaFecha,fechaActual,conn,curs,total, cantDatos, tiempoCantidad,tiempoDia)
                CrearTablasBD_XacoMeterII.borradoTablas(primeraFecha,fechaElegida,conn,curs)
                CrearTablasBD_XacoMeterII.quitaBorradoTablas(fechaElegida,fechaActual,conn,curs)
                conn.commit()
                curs.close()
                conn.close()   
                
            elif fechaElegida<primeraFecha:
                total=Destinos_XacoMeterII.buclePatrimonios(fechaElegida,primeraFecha,conn,curs,total, cantDatos, tiempoCantidad,tiempoDia)
                conn.commit()
                Destinos_XacoMeterII.buclePatrimonios(ultimaFecha,fechaActual,conn,curs,total, cantDatos, tiempoCantidad,tiempoDia)
                CrearTablasBD_XacoMeterII.quitaBorradoTablas(fechaElegida,fechaActual,conn,curs)
                conn.commit()
                curs.close()
                conn.close()

            else:
                CrearTablasBD_XacoMeterII.borradoTablas(primeraFecha,fechaElegida,conn,curs)
                Destinos_XacoMeterII.buclePatrimonios(ultimaFecha,fechaActual,conn,curs,total, cantDatos, tiempoCantidad,tiempoDia)
                CrearTablasBD_XacoMeterII.borradoTablas(ultimaFecha,fechaElegida,conn,curs)
                CrearTablasBD_XacoMeterII.quitaBorradoTablas(fechaElegida,fechaActual,conn,curs)
                conn.commit()
                curs.close()
                conn.close()
        flash('La base de datos ha sido creada correctamente')
        return redirect (url_for('home'))
    else:
        return redirect (url_for('Login'))
    
@app.route('/estadisticasTemporales/<string:patrimonio>')    
def estadisticasTemporales(patrimonio):
    graficoBarras=GraficosEstadisticas_XacoMeterII.graficoBarras(patrimonio)
    graficoCircular=GraficosEstadisticas_XacoMeterII.graficoCircularTotal(patrimonio)
    return render_template('serieTemporal.html', graficoBarras=graficoBarras, graficoCircular=graficoCircular)

def datosMapa():
    locations=pd.read_csv('.\data\inventario_01.csv',sep=';',index_col=0)   
    return locations

def cajaInformacion(localidad):
    link = "<b>%s</b><br><a href='/estadisticasTemporales/%s' target='_blank'>Estadisticas temporales</a>" % (localidad, localidad.replace(' ','+'))
    return link

if __name__ == '__main__':
    app.run(port = PORT, debug = DEBUG)
