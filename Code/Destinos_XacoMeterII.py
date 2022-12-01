import CrearTablasBD_XacoMeter
import FuncionPrincipal_XacoMeterII
import CrearTablasBD_XacoMeter
import datetime



def OperacionesBD(id, patrimonio, diccionarioBusqueda, fechaElegida):
    fechaActual = datetime.now()
    totalTweets=0
    for diferencia in range ((fechaElegida-fechaActual).days + 1):
        fechaBusqueda= fechaElegida+datetime.timedelta(days=diferencia)
        totalTweetsInsertados = FuncionPrincipal_XacoMeterII.funcionPrincipal(id,diccionarioBusqueda,fechaBusqueda)
        totalTweets += totalTweetsInsertados
    parseo = str(totalTweets)
    CrearTablasBD_XacoMeter.creaTablas(id, patrimonio)
    return ("El numero de tweets total almacenado es: "+ parseo)
    
