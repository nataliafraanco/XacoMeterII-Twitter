from os import name
import Destinos_XacoMeterII
import FuncionPrincipal_XacoMeterII
import credencialesAdmin
import Busqueda_XacoMeterII
import CrearTablasBD_XacoMeter
from flask import Flask, render_template, request, redirect
from flask_wtf import Form
from wtforms.fields import DateField
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import image
import csv
import psycopg2
import credencialesBD


app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def home ():
    if request.method=='POST':
        if request.form.get("RedecillaDelCamino"):
            diccionarioPalabras="Redecilla camino rollo justicia"
            Destinos_XacoMeterII.OperacionesBD(1,diccionarioPalabras,"RedecillaDelCamino")
            return ("Redecilla Del Camino")
        if request.form.get("Castildelgado"):
            diccionarioPalabras="Castildelgado palacio fortificado"
            Destinos_XacoMeterII.OperacionesBD(2,diccionarioPalabras,"Castildelgado")
            return ("Castildelgado")
        if request.form.get("Belorado"):
            return ("Belorado")
        if request.form.get("VillafrancaMontesDeOca"):
            diccionarioPalabras="Villafranca san felix"
            Destinos_XacoMeterII.OperacionesBD(4,diccionarioPalabras,"VillafrancaMontesDeOca")
            return ("Villafranca Montes De Oca")
        if request.form.get("SanJuanDeOrtega"):
            return ("San Juan de Ortega")
        if request.form.get("Atapuerca"):
            return ("Atapuerca")
        if request.form.get("IbeasDeJuarros"):
            return redirect("IbeasDeJuarros")
        if request.form.get("Burgos"):
            return redirect("/Burgos")
        if request.form.get("Tardajos"):
            return redirect("/Tardajos")
        if request.form.get("Hontanas"):
            return redirect("/Hontanas")
        if request.form.get("Castrojeriz"):
            return redirect("/Castrojeriz")
        if request.form.get("IteroDeLaVega"):
            return ("Itero De La Vega")
        if request.form.get("BoadillaDelCamino"):
            return redirect("/Boadilla Del Camino")
        if request.form.get("Fromista"):
            return ("Fromista")
        if request.form.get("VillacazarDeSirga"):
            return ("Villacazar De Sirga")
        if request.form.get("CarrionDeLosCondes"):
            return ("Carrion De Los Condes")
        if request.form.get("CervatosDeLaCueza"):
            return ("Cervatos De La Cueza")
        if request.form.get("Villada"):
            return ("Villada")
        if request.form.get("GrajalDeCampos"):
            return ("Grajal De Campos")
        if request.form.get("Sahagun"):
            return ("Sahagun")
        if request.form.get("MansillaDeLasMulas"):
            return ("Mansilla De Las Mulas")
        if request.form.get("VillamorosDeMansilla"):
            return ("Villamoros DeMansilla")
        if request.form.get("VillaverdeDeSandoval"):
            return ("Villaverde De Sandoval")
        if request.form.get("Leon"):
            return ("Leon")
        if request.form.get("TrobajoDelCamino"):
            return ("Trobajo Del Camino")
        if request.form.get("SanAndresDelRabanedo"):
            return ("San Andres Del Rabanedo")
        if request.form.get("LaVirgenDelCamino"):
            return ("La Virgen Del Camino")
        if request.form.get("ValverdeDeLaVirgen"):
            return ("Valverde De La Virgen")
        if request.form.get("HospitalDeOrbigo"):
            return ("Hospital De Orbigo")
        if request.form.get("SanJustoDeLaVega"):
            return ("San Justo De La Vega")
        if request.form.get("Astorga"):
            return ("Astorga")
        if request.form.get("RabanalDelCamino"):
            return ("Rabanal Del Camino")
        if request.form.get("MolinaSeca"):
            return ("Molina Seca")
        if request.form.get("Ponferrada"):
            return ("Ponferrada")
        if request.form.get("Cacabelos"):
            return ("Cacabelos")
        if request.form.get("Pieros"):
            return ("Pieros")
        if request.form.get("VillafrancaDelBierzo"):
            return ("Villafranca Del Bierzo")
        if request.form.get("VegaDeValcarce"):
            return ("Vega De Valcarce")
        if request.form.get("LaLaguna"):
            return ("La Laguna")
        
    return render_template('home.html')

@app.route("/IbeasDeJuarros",methods=['GET','POST'])
def Ibeas():
    if request.method=='POST':
        if request.form.get("CuevaDelSilo"):
            return ("Cueva del Silo")
        if request.form.get("PortalonDeEntrada"):
            return ("Cueva Mayor_01Portalon de entrada")
        if request.form.get("GPrincipalSalonDelCoro"):
            return ("Cueva Mayor_02_G. Principal Salón del Coro")
    return render_template('IbeasDeJuarros.html')
        
@app.route("/Burgos",methods=['GET','POST'])
def Burgos():
    if request.method=='POST':
        if request.form.get("ZonasDeLaCiudad"):
            return ("Determinadas zonas de la ciudad")
        if request.form.get("ArchivoHistoricoProvincial"):
            return ("Archivo Histórico Provincial")
        if request.form.get("BibliotecaPublica"):
            return ("Biblioteca Pública")
        if request.form.get("Castillo"):
            return ("Castillo")
        if request.form.get("MurallaDeBurgos"):
            return ("Muralla de Burgos")
        if request.form.get("TorreDeAlbillos"):
            return ("Torre de Albillos")
        if request.form.get("TorreDeSanZoles"):
            return ("Torre de San Zoles")
        if request.form.get("CruceroCalleNuñoRasura"):
            return ("Crucero Calle Nuño Rasura")
        if request.form.get("CruceroGamonalRioPico"):
            return ("Crucero Gamonal Rio Pico")
        if request.form.get("CruceroPlazaDelRey"):
            return ("Crucero Plaza del Rey")
        if request.form.get("ArcoDeSantaMaria"):
            return ("Arco de Santa María")
        if request.form.get("CartujaDeSantaMariaDeMiraflores"):
            return ("Cartuja de Santa María de Miraflores")
        if request.form.get("CasaDelCordon"):
            return ("Casa del Cordón")
        if request.form.get("CasaMiranda"):
            return ("Casa Miranda, Museo de Burgos")
        if request.form.get("MonasterioDeSanJuan"):
            return ("Conjunto del Monasterio de San Juan")
        if request.form.get("ConsuladoDelMar"):
            return ("Cosulado del Mar")
        if request.form.get("HospitalDeLaConcepcion"):
            return ("Hospital de la Concepción")
        if request.form.get("HospitalDelRey"):
            return ("Hospital del Rey")
        if request.form.get("IglesiaCatedralDeSantaMaria"):
            return ("Iglesia Catedral de Santa María")
        if request.form.get("IglesiaDeSanEsteban"):
            return ("Iglesia de San Esteban")
        if request.form.get("Leon"):
            return ("Iglesia de San Gil")
        if request.form.get("Leon"):
            return ("Iglesia de San Nicolás de Bari")
        if request.form.get("IglesiaDeSantaMaria"):
            return ("Iglesia de Santa María")
        if request.form.get("MonasterioDeSantaMariaDeLasHuelgas"):
            return ("Monasterio de Santa María la Real de las Huelgas")
        if request.form.get("MuseoRealMonasterioDeLasHuelgas"):
            return ("Museo del Real Monasterio de las Huelgas")
        if request.form.get("PalacioAngulo"):
            return ("Palacio Angulo, exclusivamente fachada, Museo de Burgos")
        if request.form.get("PalacioPaseoDeLaIsla"):
            return ("Palacio del Paseo de la Isla")
        if request.form.get("PuertaSanEsteban"):
            return ("Puerta de San Esteban")
        if request.form.get("MonasterioSanAgustin"):
            return ("Real Monasterio de San Agustín")
        if request.form.get("TeatroPrincipal"):
            return ("Teatro Principal")
        if request.form.get("CatedralDeBurgos"):
            return ("Teatro Principal")
            diccionarioPalabras="Catedral de Burgos"
            #resultado = Destinos_XacoMeterII.OperacionesBD(30,diccionarioPalabras)
            #return (resultado)

    return render_template('Burgos.html')

@app.route("/Tardajos",methods=['GET','POST'])
def Tardajos():
    if request.method=='POST':
        if request.form.get("Crucero"):
            return ("Crucero")
        if request.form.get("YacimientoDeDeobrigula"):
            return ("Yacimiento de Deobrigula")
    return render_template('Tardajos.html')

@app.route("/Hontanas",methods=['GET','POST'])
def Hontanas():
    if request.method=='POST':
        if request.form.get("Crucero"):
            return ("Crucero")
        if request.form.get("TorreonDeHontanas"):
            return ("Torreon de Hontanas")
    return render_template('Hontanas.html')

@app.route("/Castrojeriz",methods=['GET','POST'])
def Castrojeriz():
    if request.method=='POST':
        if request.form.get("LaVilla"):
            return ("La Villa")
        if request.form.get("ElFuerte"):
            return ("Casa Guitiérrez Barona o El Fuerte")
        if request.form.get("CastilloDeCastrojeriz"):
            return ("Castillo de Castrojeriz")
        if request.form.get("LaTorre"):
            return ("La Torre")
        if request.form.get("Murallas"):
            return ("Murallas")
        if request.form.get("IglesiaColegiataSantaMaríaDelManzano"):
            return ("Iglesia Colegiata Santa María del Manzano")
        if request.form.get("IglesiaDeSanJuan"):
            return ("Iglesia de San Juan")
    return render_template('Castrojeriz.html')

@app.route("/BoadillaDelCamino",methods=['GET','POST'])
def BoadillaDelCamino():
    if request.method=='POST':
        if request.form.get("CanalDeCastilla"):
            return ("Canal de Castilla")
        if request.form.get("IglesiaParroquialDeNuestraSeñoraDeLaAsuncion"):
            return ("Iglesia parroquial de Nuestra Señora de la Asunción")
        if request.form.get("RolloDeJusticiaDeLaVilla"):
            return ("Rollo de Justicia de la Villa")
    return render_template('BoadillaDelCamino.html')

@app.route('/login')
def Login():
    return render_template('login.html')
@app.route('/login', methods = ['POST'])
def LoginComprobante():
    usuario = request.form.get ('usuario')
    contraseña = request.form.get ('contraseña')
    if request.form.get('recordar'):
        recordar = True
    else:
        recordar = False
           
    if ((usuario == credencialesAdmin.usuario) and (contraseña == credencialesAdmin.contraseña)):
        return redirect("/Administrador")
    
    else:
        return ('Vuelva a intentarlo')
    
@app.route('/Administrador')
def Administrador():
    return render_template('admin.html')
@app.route('/Administrador', methods = ['POST'])
def AdministradorOpciones():
    diccionarioBusqueda = Busqueda_XacoMeterII.palabrasClave()
    if request.form.get('actualizar'):
        for x, y in diccionarioBusqueda.items():
            index = CrearTablasBD_XacoMeter.actualizaTablas(x)
            print(index)
            #Hacer conexion con la base de datos y si coincide el nombre del patrimonio con la base de datos coger ese index
            Destinos_XacoMeterII.OperacionesBD(index, x, y)
        return ("La base de datos ha sido actualizada")
    if request.form.get('crear'):
        return redirect ('/Administrador/CrearBaseDeDatos')
@app.route('/Administrador/CrearBaseDeDatos')
def eligeFecha():
    calendario = CalendarioForm()
    return render_template ("admin_Crear.html", form = calendario)
@app.route('/Administrador/CrearBaseDeDatosFecha')
def AdministradorCrear():
    fecha = request.form["fechaElegida"]
    diccionarioBusqueda = Busqueda_XacoMeterII.palabrasClave()
    conn = psycopg2.connect(host="localhost",database="XacoMeter",port=5432,user=credencialesBD.USUARIO,password=credencialesBD.CONTRASEÑA)
    curs = conn.cursor()
    curs.execute('DROP TABLE IF EXISTS LISTADO_PATRIMONIOS CASCADE') 
    curs.execute('DROP TABLE IF EXISTS TWEETS_PATRIMONIOS') 
    conn.commit()
    curs.close()
    conn.close()
    index = 1
    for x, y in diccionarioBusqueda.items():
        Destinos_XacoMeterII.OperacionesBD(index, x, y, fecha)
        index += 1

'''@app.route('/Administrador/CrearBaseDeDatosFecha', methods = ['POST'])
def AdministradorCrearPost():
    return("La base de datos ha sido creada correctamente ")
    '''
class CalendarioForm(Form):
    fechaElegida = DateField ('DatePicker', format='yyyy-MM-DD')
        
        
        




