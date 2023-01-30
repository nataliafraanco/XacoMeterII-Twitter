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