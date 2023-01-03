import CrearTablasBD_XacoMeterII
import FuncionPrincipal_XacoMeterII
import Busqueda_XacoMeterII
import datetime
import time


def OperacionesBD(id, patrimonio, diccionarioBusqueda, primeraFecha, ultimaFecha, contador,conn,curs, cantDatos, tiempoCantidad,tiempoDia):
    #ultimaFecha = datetime.datetime.now()
    #Realiza tantas consultas como días haya de diferencia entre la fecha seleccionada y la fecha actual
    consultas=(ultimaFecha-primeraFecha).days
    for diferencia in range (consultas):
        fechaBusqueda= primeraFecha+datetime.timedelta(days=diferencia)
        fechaFin= fechaBusqueda+datetime.timedelta(days=1)
        fechaBusqueda = fechaBusqueda.strftime("%Y-%m-%dT%H:%M:%SZ")
        fechaFin = fechaFin.strftime("%Y-%m-%dT%H:%M:%SZ")
        print(fechaBusqueda, fechaFin)
        time.sleep(tiempoDia)
        contador+=1
        #El API de Twitter permite 300 consultas cada 15 minutos, en el caso de caso de llegar a ellas, hacemos una parada de 5 minutos
        if contador == cantDatos:
            time.sleep(tiempoCantidad)
            contador=0
        FuncionPrincipal_XacoMeterII.funcionPrincipal(id,diccionarioBusqueda,fechaBusqueda,fechaFin)
    CrearTablasBD_XacoMeterII.insertaDatos(id, patrimonio,conn,curs)
    print ('---', contador)
    return contador

def buclePatrimonios(primeraFecha,ultimaFecha,conn,curs, total, cantDatos, tiempoCantidad,tiempoDia):
    
    diccionarioBusqueda = Busqueda_XacoMeterII.palabrasClave()
    for x, y in diccionarioBusqueda.items():
            index = CrearTablasBD_XacoMeterII.actualizaTablas(x,conn,curs)[0][0]
            total = OperacionesBD(index, x, y, primeraFecha,ultimaFecha, total,conn,curs,cantDatos, tiempoCantidad,tiempoDia)
            if total == cantDatos:
                time.sleep(tiempoCantidad)
                total=0
            print (total)
    return total
