from fastapi import APIRouter
from app.models.schemas import ChatRequest
from app.services.chatbot_service import get_response

router = APIRouter()

@router.post("/chat")
def chat(req: ChatRequest):
    return {"response": get_response(req.user_id, req.message)}