from fastapi import FastAPI
from transformers import pipeline

app = FastAPI() #chama o Fast APi

sentiment_analyzer =  pipeline("sentiment-analysis") # biblioteca que analisa sentimentos da transformers

@app.get("/")
def home():
    return {"message": "API de analise de Sentimentos"} #verifica se ta funcionando API

@app.post("/analyze/")
def analyze_sentiment(text: str): #funcao recebe um texto para analisar
    result = sentiment_analyzer(text) #chama a biblioteca
    #retorna o mesmo com a analise e a confiança
    return{"text": text, "sentiment": result[0]["label"], "confidence": result[0]["score"]}
    