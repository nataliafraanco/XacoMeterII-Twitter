from os import name
import time
import Destinos_XacoMeterII
import Busqueda_XacoMeterII
import CrearTablasBD_XacoMeter
from flask import Flask, render_template, request, redirect, session, flash, url_for
import psycopg2
import psycopg2.extras
import credencialesBD
import datetime
from datetime import datetime,timedelta
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'Secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta (minutes = 30)
DEBUG = False
PORT = 5000

@app.route("/",methods=['GET','POST'])
def home ():        
    return render_template('home.html')
  
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
        ultimaFecha = CrearTablasBD_XacoMeter.ultimaFecha2(conn,curs)[0][0]
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
        primeraFecha=CrearTablasBD_XacoMeter.primeraFecha(conn,curs)[0][0]
        ultimaFecha=CrearTablasBD_XacoMeter.ultimaFecha2(conn,curs)[0][0]
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
                CrearTablasBD_XacoMeter.borradoTablas(primeraFecha,fechaElegida,conn,curs)
                CrearTablasBD_XacoMeter.quitaBorradoTablas(fechaElegida,fechaActual,conn,curs)
                conn.commit()
                curs.close()
                conn.close()   
                
            elif fechaElegida<primeraFecha:
                total=Destinos_XacoMeterII.buclePatrimonios(fechaElegida,primeraFecha,conn,curs,total, cantDatos, tiempoCantidad,tiempoDia)
                conn.commit()
                Destinos_XacoMeterII.buclePatrimonios(ultimaFecha,fechaActual,conn,curs,total, cantDatos, tiempoCantidad,tiempoDia)
                CrearTablasBD_XacoMeter.quitaBorradoTablas(fechaElegida,fechaActual,conn,curs)
                conn.commit()
                curs.close()
                conn.close()

            else:
                CrearTablasBD_XacoMeter.borradoTablas(primeraFecha,fechaElegida,conn,curs)
                Destinos_XacoMeterII.buclePatrimonios(ultimaFecha,fechaActual,conn,curs,total, cantDatos, tiempoCantidad,tiempoDia)
                CrearTablasBD_XacoMeter.borradoTablas(ultimaFecha,fechaElegida,conn,curs)
                CrearTablasBD_XacoMeter.quitaBorradoTablas(fechaElegida,fechaActual,conn,curs)
                conn.commit()
                curs.close()
                conn.close()
        flash('La base de datos ha sido creada correctamente')
        return redirect (url_for('home'))
    else:
        return redirect (url_for('Login'))
'''
@app.errorhandler 
'''
if __name__ == '__main__':
    app.run(port = PORT, debug = DEBUG)
