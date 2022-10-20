import FuncionPrincipal_XacoMeterII
from flask import Flask, render_template
import wordcloud
import matplotlib.pyplot


app = Flask(__name__)
@app.route("/")
def HOME ():
    return "<p>XACOMETER 2.0</p>"

@app.route("/CatedralBurgos")
def CatedralBurgos():
    Resultado=FuncionPrincipal_XacoMeterII.principal_function("Catedral Burgos")
    totalTweetsInsertados = FuncionPrincipal_XacoMeterII.insert_data(Resultado, "Catedral_Burgos.csv")
    parseo = str(totalTweetsInsertados)
    return ("El numero de tweets total almacenado es: "+ parseo)