#organizar em ordem alfabetica as biblioteca!!!!!!!!!!!!!!!!!!!!!!
from fastapi import FastAPI
from pydantic import BaseModel #pydantic serve para validação de dados
from transformers import pipeline

#------------------------------------------------------------------------------#


app = FastAPI() #chama o Fast APi

sentiment_analyzer =  pipeline("sentiment-analysis") # biblioteca que analisa sentimentos da transformers

#Essa class é basicamente um Struct em C
class TextInput(BaseModel): #BaseModel é uma forma de Bolo, que vai garantir que o bolo vai sair redondo
        text: str #vai esperar resposta do tipo string

@app.get("/")
def home():
    return {"message": "API de analise de Sentimentos"} #verifica se ta funcionando API

@app.post("/analyze/")
#Agora é possível receber um Json.
def analyze_sentiment(input_data: TextInput): #input_data é do tipo TextInput
    result = sentiment_analyzer(input_data.text) 
    return{"text":input_data.text, 
           "sentiment": result[0]["label"],
           "confidence": round(result[0]["score"],  4)}
    