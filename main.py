#organizar em ordem alfabetica as biblioteca!!!!!!!!!!!!!!!!!!!!!!
from fastapi import FastAPI, HTTPException,Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel #pydantic serve para validação de dados
from transformers import pipeline

#------------------------------------------------------------------------------#

app = FastAPI() #chama o Fast APi

try:
    sentiment_analyzer =  pipeline("sentiment-analysis") # biblioteca que analisa sentimentos da transformers
except Exception as e:
    raise HTTPException(status_code=500, detail = f"Erro ao carregar o modelo")




#Essa class é basicamente um Struct em C
class TextInput(BaseModel): #BaseModel é uma forma de Bolo, que vai garantir que o bolo vai sair redondo
        text: str #vai esperar resposta do tipo string


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,  
        content={"detail": "Erro no formato de texto, Não esta em JSON"}
    )

@app.post("/analyze/")
#Agora é possível receber um Json.
def analyze_sentiment(input_data: TextInput): #input_data é do tipo TextInput
 try:
    result = sentiment_analyzer(input_data.text) 
    return{"text":input_data.text, 
           "sentiment": result[0]["label"],
           "confidence": round(result[0]["score"],  4)}
 except ValueError as e:
    raise HTTPException(status_code=500, detail = f"Erro ao processar a análise de sentimento.")

    