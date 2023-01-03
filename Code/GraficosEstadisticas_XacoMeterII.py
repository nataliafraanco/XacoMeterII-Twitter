import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import psycopg2
from datetime import datetime,timedelta
import credencialesBD
import CrearTablasBD_XacoMeterII

def graficoBarras(patrimonio):
    patrimonio = str(patrimonio.replace('+',' '))
    print(patrimonio)
    conn = psycopg2.connect(host="localhost",database="XacoMeter",port=5432,user=credencialesBD.USUARIO,password=credencialesBD.CONTRASEÑA)
    curs = conn.cursor()
    primeraFecha=CrearTablasBD_XacoMeterII.primeraFecha(conn,curs)[0][0]
    ultimaFecha=CrearTablasBD_XacoMeterII.ultimaFecha2(conn,curs)[0][0]
    consultas=(ultimaFecha-primeraFecha).days
    fechas=[]
    datos=[]
    for diferencia in range (consultas):
        fechaBusqueda= primeraFecha+timedelta(days=diferencia)
        fechaBD = fechaBusqueda.strftime("%Y-%m-%d")
        numeroDatos = CrearTablasBD_XacoMeterII.cuentaDatos(conn,curs,fechaBD,patrimonio)
        fechas.append(fechaBD)
        datos.append(numeroDatos)
    plt.plot(fechas,datos)
    plt.xticks(rotation=45)
    plt.xlabel('Fechas')
    plt.ylabel('Número de tweets')
    plt.tight_layout()
    plt.title('Tweets de ', patrimonio, ' entre ', primeraFecha, ' y ', ultimaFecha)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graficoBarras = base64.b64encode(buffer.getvalue()).decode('utf-8')
    #buffer.close
    #buffer.flush
    return graficoBarras

def graficoCircularTotal(patrimonio):
    patrimonio = str(patrimonio.replace('+',' '))
    print(patrimonio)
    conn = psycopg2.connect(host="localhost",database="XacoMeter",port=5432,user=credencialesBD.USUARIO,password=credencialesBD.CONTRASEÑA)
    curs = conn.cursor()
    tweets=[]
    nombres=['Total',patrimonio]
    primeraFecha=CrearTablasBD_XacoMeterII.primeraFecha(conn,curs)[0][0]
    ultimaFecha=CrearTablasBD_XacoMeterII.ultimaFecha2(conn,curs)[0][0]
    tweets.append(CrearTablasBD_XacoMeterII.cuentaFilas(conn,curs,primeraFecha,ultimaFecha))
    tweets.append(CrearTablasBD_XacoMeterII.cuentaFilasPatrimonio(conn,curs,primeraFecha,ultimaFecha,patrimonio)) 
    plt.pie(tweets, nombres,explode=(0, 0.2))
    plt.title('Porcentaje de tweets de ', patrimonio, ' respecto al total recopilados entre ', primeraFecha, ' y ', ultimaFecha)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graficoCircular = base64.b64encode(buffer.getvalue()).decode('utf-8')
    #buffer.close
    #buffer.flush
    return graficoCircular