import FuncionPrincipal_XacoMeterII
import InsertarDatosBD_XacoMeter


@app.route("/Burgos",methods=['GET','POST'])
def CatedralBurgos():
    #Si no existe, crea una entrada en la base de datos en la tabla LISTADO_PATRIMONIOS
    #InsertarDatosBD_XacoMeter.insertar_TablaPatrimonio(1,'Catedral de Burgos')
    #Resultado=FuncionPrincipal_XacoMeterII.principal_function("Catedral Burgos")
    #totalTweetsInsertados = FuncionPrincipal_XacoMeterII.insert_data(Resultado, "Catedral_Burgos.csv")
    #parseo = str(totalTweetsInsertados)
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
    #return ("El numero de tweets total almacenado es: "+ parseo)
    return FuncionPrincipal_XacoMeterII.principal_function("Catedral Burgos")