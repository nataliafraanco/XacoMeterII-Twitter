import pandas as pd
import matplotlib as plt
from wordcloud import WordCloud
import CrearTablasBD_XacoMeter
import FuncionPrincipal_XacoMeterII
import CrearTablasBD_XacoMeter



def OperacionesBD(id, patrimonio):
    totalTweetsInsertados = FuncionPrincipal_XacoMeterII.funcionPrincipal(id,patrimonio)
    parseo = str(totalTweetsInsertados)
    CrearTablasBD_XacoMeter.creaTablas(id, patrimonio)
    """
    data = pd.read_csv(r"Catedral_Burgos.csv", encoding ="UTF-8")
    comment_words=""
    for i in data:
        i = str(i)
        separate = i.split()
        for j in range(len(separate)):
            separate[j] = separate[j].lower()
        comment_words += " ".join(separate)+" "
        
    final_wordcloud = WordCloud(width = 800, height = 800, max_words=20,
                background_color ='black', 
                #stopwords = stop_words, 
                min_font_size = 1).generate(comment_words)
    
    plt.figure(figsize = (5, 5), facecolor = None)
    plt.imshow(final_wordcloud)
    plt.axis("off")
    plt.show()
    """
    return ("El numero de tweets total almacenado es: "+ parseo)
    
