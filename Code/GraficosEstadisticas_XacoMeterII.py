import matplotlib
matplotlib.use('Agg')
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime,timedelta
import Code.CrearTablasBD_XacoMeterII
import matplotlib.dates as mdates
import plotly
import json
import plotly.graph_objects as go
from plotly.offline import plot
import pandas as pd
import plotly.express as px
'''
def graficoTemporal(patrimonio, primeraFecha, ultimaFecha, conn, curs):
    plt.figure(figsize=(8,4))
    plt.clf()
    plt.tight_layout()
    patrimonio = str(patrimonio.replace('+',' '))
    print(patrimonio)
    consultas=(ultimaFecha-primeraFecha).days
    fechas=[]
    datos=[]
    for diferencia in range (consultas):
        fechaBusqueda= primeraFecha+timedelta(days=diferencia)
        fechaBD = fechaBusqueda.strftime("%Y-%m-%d")
        datos.append(Code.CrearTablasBD_XacoMeterII.cuentaDatos(conn,curs,fechaBD,patrimonio))
        fechas.append(fechaBD)
    fechas_datetime = [datetime.strptime(f, '%Y-%m-%d') for f in fechas]
    plt.plot(fechas_datetime, datos)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    plt.xlabel('Fechas')
    plt.ylabel('Número de tweets')
    plt.title('Tweets de '+ patrimonio)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graficoBarras = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.flush
    return graficoBarras

def graficoCircularTotal(patrimonio, primeraFecha, ultimaFecha, conn, curs):
    plt.clf()
    plt.tight_layout()
    patrimonio = str(patrimonio.replace('+',' '))
    print(patrimonio)
    tweets=[]
    tweets.append(Code.CrearTablasBD_XacoMeterII.cuentaFilas(conn,curs,primeraFecha,ultimaFecha)[0])
    tweets.append(Code.CrearTablasBD_XacoMeterII.cuentaFilasPatrimonio(conn,curs,primeraFecha,ultimaFecha,patrimonio)[0]) 
    if tweets[0] != 0 and tweets[0] != None:
        porcentaje=round(((tweets[1]*100)/tweets[0]), 2)
    else:
        porcentaje=0
    resto=100-porcentaje
    nombres=['Otros = '+ str(resto)+'%', 'Patrimonio = '+ str(porcentaje)+'%']
    plt.pie(tweets, labels=nombres)
    plt.title('Porcentaje de tweets de '+ patrimonio + ' respecto al total')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graficoCircular = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.flush
    return graficoCircular

def graficoMetricasPublicas(patrimonio, primeraFecha, ultimaFecha, conn, curs):

    plt.clf()
    plt.tight_layout()
    patrimonio = str(patrimonio.replace('+',' '))
    print(patrimonio)
    likes=[]
    retweets=[]
    reply=[]
    consultas=(ultimaFecha-primeraFecha).days
    fechas=[]
    for diferencia in range (consultas):
        fechaBusqueda= primeraFecha+timedelta(days=diferencia)
        fechaBD = fechaBusqueda.strftime("%Y-%m-%d")
        likes.append(Code.CrearTablasBD_XacoMeterII.cuentaLikes(conn,curs,fechaBD,patrimonio))
        reply.append(Code.CrearTablasBD_XacoMeterII.cuentaReply(conn,curs,fechaBD,patrimonio))
        retweets.append(Code.CrearTablasBD_XacoMeterII.cuentaRetweet(conn,curs,fechaBD,patrimonio))  
        fechas.append(fechaBD)
    fechas_datetime = [datetime.strptime(f, '%Y-%m-%d') for f in fechas]
    plt.figure(figsize=(18,4))
    plt.bar(fechas_datetime,likes,color="green",label="LIKES")
    plt.bar(fechas_datetime,reply,color="yellow",bottom=likes,label="RESPUESTAS")
    plt.bar(fechas_datetime,retweets,color="red", label="RETWEETS", bottom=[i+j for i,j in zip(likes, reply)])
    plt.legend(loc="upper right",bbox_to_anchor=(0.8,1.0))
    plt.title('Likes, Respuestas y Retweets de '+ patrimonio)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    plt.xlabel('Fechas')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graficoMetricasPublicas = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.flush
    return graficoMetricasPublicas'''
    
def graficoLineas(dfdiccionarioDatos):
    fechas = dfdiccionarioDatos['date'].to_numpy()
    print(fechas)
    filas = dfdiccionarioDatos['filas'].to_numpy()
    print(filas)
    graficoLineas=go.Layout(title='Gráfico de lineas')
    figuraLineas=go.Figure(data=[go.Scatter(x=fechas,y=filas)], layout=graficoLineas)
    graficoLineasJSON = json.dumps(figuraLineas, cls=plotly.utils.PlotlyJSONEncoder)
    return graficoLineasJSON

def graficoCircular(dfdiccionarioDatos, total):
    datos=[]
    filasPatrimonio = sum(dfdiccionarioDatos['filas'].to_numpy())
    print(filasPatrimonio)
    total=total[0]-filasPatrimonio
    datos.append(filasPatrimonio)
    datos.append(total)
    etiquetas=['patrimonio','total']
    graficoCircular=go.Layout(title='Gráfico Circular')
    figuraCircular=go.Figure(data=[go.Pie(labels=etiquetas, values=datos,pull=[0, 0.2])], layout=graficoCircular)
    graficoCircularJSON = json.dumps(figuraCircular, cls=plotly.utils.PlotlyJSONEncoder)
    return graficoCircularJSON

def graficoBarras(dfdiccionarioDatos, total):
    figuraBarras = px.bar(dfdiccionarioDatos, x="date", y=["rp","like","rt"])
    graficoBarrasJSON = json.dumps(figuraBarras, cls=plotly.utils.PlotlyJSONEncoder)
    return graficoBarrasJSON