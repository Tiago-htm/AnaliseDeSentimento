from fastapi import FastAPI, HTTPException,Request,Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel #pydantic serve para validação de dados
from sqlalchemy.orm import Session
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
#Meus imports
from database import get_db, engine
from models import Base, SentimentAnalysis
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
##Banco
Base.metadata.create_all(bind=engine) 

#------------------------------------------------------------------------------#
app = FastAPI() #chama o Fast APi

#  isso é CORS serve para permitir que o front converse com o a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  #endereço da minha aplicação
    allow_credentials=True,
    allow_methods=["*"], #permite todos os methodos
    allow_headers=["*"],  
)



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
def analyze_sentiment(input_data: TextInput, db: Session = Depends(get_db)): #input_data é do tipo TextInput
 try:
    result = sentiment_analyzer(input_data.text) 
    sentiment = result[0]["label"]
    confidence = round(result[0]["score"], 4)

    sentiment_record = SentimentAnalysis(text=input_data.text,sentiment=sentiment, confidence=confidence)
    db.add(sentiment_record)
    db.commit() ## envia os dados para banco para salvar   
    db.refresh(sentiment_record)
    return{
            "id": sentiment_record.id,
            "text": sentiment_record.text,
            "sentiment": sentiment_record.sentiment,
            "confidence": sentiment_record.confidence,
          }
 

 except Exception as e:
    raise HTTPException(status_code=500, detail = f"Erro ao processar a análise de sentimento.")

