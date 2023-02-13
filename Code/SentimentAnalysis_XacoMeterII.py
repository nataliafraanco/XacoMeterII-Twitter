from sentiment_analysis_spanish import sentiment_analysis

def SentimentAnalysis(conn,curs):
    #Crea todos los índices de sentimientos cuando se crea la columna
    sentiment = sentiment_analysis.SentimentAnalysisSpanish()
    curs.execute("SELECT Tweet_Id, Tweet_Texto FROM TWEETS_PATRIMONIOS")
    filas=curs.fetchall()
    for row in filas:
        id = row[0]
        texto = row[1]
        sentimiento = sentiment.sentiment(texto)
        curs.execute("UPDATE TWEETS_PATRIMONIOS SET Tweet_SentimentAnalysis = %s WHERE Tweet_Id = %s", (sentimiento, id))
        conn.commit()
        
     
def SentimentAnalysisPatrimonio(conn,curs):
    #Crea todos los índices de sentimientos cuando el valor es NULL
    sentiment = sentiment_analysis.SentimentAnalysisSpanish()
    curs.execute("SELECT Tweet_Id, Tweet_Texto FROM TWEETS_PATRIMONIOS WHERE Tweet_SentimentAnalysis is NULL;")
    filas=curs.fetchall()
    for row in filas:
        id = row[0]
        texto = row[1]
        sentimiento = sentiment.sentiment(texto)
        curs.execute("UPDATE TWEETS_PATRIMONIOS SET Tweet_SentimentAnalysis = %s WHERE Tweet_Id = %s", (sentimiento, id))
    conn.commit()
    
    

    
