import FuncionPrincipal_XacoMeterII
from flask import Flask, render_template
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import image
import csv


app = Flask(__name__)
@app.route("/")
def HOME ():
    return "<p>XACOMETER 2.0</p>"

@app.route("/CatedralBurgos")
def CatedralBurgos():
    Resultado=FuncionPrincipal_XacoMeterII.principal_function("Catedral Burgos")
    totalTweetsInsertados = FuncionPrincipal_XacoMeterII.insert_data(Resultado, "Catedral_Burgos.csv")
    parseo = str(totalTweetsInsertados)
    
    data = pd.read_csv(r"Catedral_Burgos.csv", encoding ="latin-1")
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
                min_font_size = 10).generate(comment_words)
    #plt.figure(figsize = (5, 5), facecolor = None)
    #plt.imshow(final_wordcloud)
    #plt.show()
    return ("El numero de tweets total almacenado es: "+ parseo)


    #mask = np.array(image.open("letra_T.jpg"))
    #mask[mask == 1] = 255
    '''
    your_list = []
    with open('Catedral_Burgos.csv', 'rb') as f:
        reader = csv.reader(f)
        your_list = '\t'.join([i[5] for i in reader])
        #background_color = "white", max_words = 50, mask = mask
    wordcloud = wc().generate(your_list)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
   

#def wCloud():
    '''