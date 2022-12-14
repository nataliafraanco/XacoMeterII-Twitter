import CrearTablasBD_XacoMeter
import FuncionPrincipal_XacoMeterII
import Busqueda_XacoMeterII
import CrearTablasBD_XacoMeter
import datetime
import time


def OperacionesBD(id, patrimonio, diccionarioBusqueda, primeraFecha, ultimaFecha, contador,conn,curs):
    #ultimaFecha = datetime.datetime.now()
    #Realiza tantas consultas como días haya de diferencia entre la fecha seleccionada y la fecha actual
    consultas=(ultimaFecha-primeraFecha).days
    for diferencia in range (consultas):
        fechaBusqueda= primeraFecha+datetime.timedelta(days=diferencia)
        fechaFin= fechaBusqueda+datetime.timedelta(days=1)
        fechaBusqueda = fechaBusqueda.strftime("%Y-%m-%dT%H:%M:%SZ")
        fechaFin = fechaFin.strftime("%Y-%m-%dT%H:%M:%SZ")
        print(fechaBusqueda, fechaFin)
        FuncionPrincipal_XacoMeterII.funcionPrincipal(id,diccionarioBusqueda,fechaBusqueda,fechaFin)
        time.sleep(1)
        contador+=1
        #El API de Twitter permite 300 consultas cada 15 minutos, en el caso de caso de llegar a ellas, hacemos una parada de 5 minutos
        if contador == 299:
            time.sleep(60*10)
            contador=0
    CrearTablasBD_XacoMeter.insertaDatos(id, patrimonio,conn,curs)
    print ('---', contador)
    return contador

def buclePatrimonios(primeraFecha,ultimaFecha,conn,curs):
    total = 0
    diccionarioBusqueda = Busqueda_XacoMeterII.palabrasClave()
    for x, y in diccionarioBusqueda.items():
            index = CrearTablasBD_XacoMeter.actualizaTablas(x,conn,curs)[0][0]
            print(index)
            total = OperacionesBD(index, x, y, primeraFecha,ultimaFecha, total,conn,curs)
            if total == 299:
                time.sleep(60*10)
                total=0
            print (total)
