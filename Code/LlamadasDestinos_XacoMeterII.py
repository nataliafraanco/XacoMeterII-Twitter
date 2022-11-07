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
            return ("Ibeas De Juarros")
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

@app.route("/Burgos",methods=['GET','POST'])
def Burgos():
    if request.method=='POST':
        if request.form.get("CatedralDeBurgos"):
            return FuncionPrincipal_XacoMeterII.principal_function("Catedral Burgos")
        if request.form.get("Leon"):
            return ("Leon")
        
    return render_template('Burgos.html')
    






