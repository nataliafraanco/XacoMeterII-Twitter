import io
import base64
from datetime import datetime,timedelta
import Code.CrearTablasBD_XacoMeterII
import plotly
import json
import plotly.graph_objects as go
from plotly.offline import plot
import pandas as pd
import plotly.express as px

def graficoLineas(dfdiccionarioDatos,patrimonio):
    #Crea con plotly el gráfico de lineas
    fechas = dfdiccionarioDatos['Fechas'].to_numpy()
    filas = dfdiccionarioDatos['Filas'].to_numpy()
    graficoLineas=go.Layout(title='Tweets por día de '+patrimonio)
    figuraLineas=go.Figure(data=[go.Scatter(x=fechas,y=filas)], layout=graficoLineas)
    graficoLineasJSON = json.dumps(figuraLineas, cls=plotly.utils.PlotlyJSONEncoder)
    return graficoLineasJSON

def graficoCircular(dfdiccionarioDatos, total, patrimonio):
    #Crea con plotly el gráfico circular
    datos=[]
    filasPatrimonio = sum(dfdiccionarioDatos['Filas'].to_numpy())
    total=total[0]-filasPatrimonio
    datos.append(filasPatrimonio)
    datos.append(total)
    etiquetas=['BIC de'+patrimonio,'Otros BICs']
    graficoCircular=go.Layout(title='Porcentaje de tweets de '+patrimonio)
    figuraCircular=go.Figure(data=[go.Pie(labels=etiquetas, values=datos,pull=[0, 0.2])], layout=graficoCircular)
    graficoCircularJSON = json.dumps(figuraCircular, cls=plotly.utils.PlotlyJSONEncoder)
    return graficoCircularJSON

def graficoBarras(dfdiccionarioDatos, patrimonio):
    #Crea con plotly el gráfico de barras apiladas
    figuraBarras = px.bar(dfdiccionarioDatos, x="Fechas", y=["Reply","Like","Retweet"], title="Metricas públicas por día de "+patrimonio)
    graficoBarrasJSON = json.dumps(figuraBarras, cls=plotly.utils.PlotlyJSONEncoder)
    return graficoBarrasJSON

def graficoGeneral(dfdiccionarioDatos, fechaInicio, fechaFin):
    #Crea con plotly el gráfico de barras general
    figuraBarrasGeneral=px.bar(dfdiccionarioDatos,y='Patrimonio',x='Filas', height=20*dfdiccionarioDatos.shape[0],
                labels={'Filas':'Tweets','Patrimonio':'BICs'})
    graficoBarrasGeneralJSON = json.dumps(figuraBarrasGeneral, cls=plotly.utils.PlotlyJSONEncoder)
    return graficoBarrasGeneralJSON
    
def Sentiment_Analysis(dfdiccionarioDatos):
    #Crea con plotly el gráfico de análisis de sentimientos
    filasPatrimonio = sum(dfdiccionarioDatos['Filas'].to_numpy())
    sentimientoTotal = float(sum(dfdiccionarioDatos['Sentimiento'].to_numpy()))
    sentimientoMedio=0
    if filasPatrimonio!=0:
        sentimientoMedio = sentimientoTotal/filasPatrimonio
    analisisSentimiento=go.Layout(title='Análisis de sentimientos')
    figuraSentimientos = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = sentimientoMedio,
        mode = "gauge+number+delta",
        gauge = {'axis': {'range': [None, 1], 
                'tickcolor': "blue"}, 
                'bar': {'color': "darkblue"},
                'steps' : [
                    {'range': [0, 0.2], 'color': "red"},
                    {'range': [0.2, 0.4], 'color': "salmon"},
                    {'range': [0.4, 0.6], 'color': "yellow"},
                    {'range': [0.6, 0.8], 'color': "lightgreen"},
                    {'range': [0.8, 1], 'color': "green"}]
               }), layout=analisisSentimiento)
    graficoBarrasGeneralJSON = json.dumps(figuraSentimientos, cls=plotly.utils.PlotlyJSONEncoder)
    return graficoBarrasGeneralJSON
    