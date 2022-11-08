from os import name
import Destinos_XacoMeterII
import FuncionPrincipal_XacoMeterII
from flask import Flask, render_template, request, redirect
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import image
import csv


app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def HOME ():
    if request.method=='POST':
        if request.form.get("RedecillaDelCamino"):
            return ("Redecilla Del Camino")
        if request.form.get("Castildelgado"):
            return ("Castildelgado")
        if request.form.get("Belorado"):
            return ("Belorado")
        if request.form.get("VillafrancaMontesDeOca"):
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
            return ("Tardajos")
        if request.form.get("Hontanas"):
            return ("Hontanas")
        if request.form.get("Castrojeriz"):
            return ("Castrojeriz")
        if request.form.get("IteroDeLaVega"):
            return ("Itero De La Vega")
        if request.form.get("BoadillaDelCamino"):
            return ("Boadilla Del Camino")
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
            return FuncionPrincipal_XacoMeterII.principal_function("Catedral Burgos")
        
    return render_template('Burgos.html')
    






