from fastapi import APIRouter
from chatbot import chatbot
from pydantic import BaseModel

api = APIRouter()

class UserMessage(BaseModel):
    message: str

@api.post("/get-response")
async def get_response(user_message: UserMessage):
    response = chatbot.get_response(user_message.message)
    return {"response": str(response)}
