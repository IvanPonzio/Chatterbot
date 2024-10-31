from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.chatbot import obtener_respuesta  # Importar desde chatbot.py

app = FastAPI()

# Habilitar CORS
origins = [
    "http://localhost:3000",  # URL de tu frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

@app.post("/get-response")
async def get_response(message: Message):
    try:
        respuesta = obtener_respuesta(message.message)
        return {"response": respuesta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
