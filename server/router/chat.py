from fastapi import APIRouter

from server.modules.chat.dtos.request import ChatRequest
from server.modules.chat.dtos.response import ChatResponse
from server.modules.chat.services.chatbot import get_chat_response
from server.common.logging.config import setup_logging

logger = setup_logging(__name__)

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) :
    try:
        # 질문에 대한 답변 생성
        generated_text = get_chat_response(
            collection_name="PRODUCTS", 
            llm_model=request.model,
            messages=request.messages,
        )

        # 답변 전달
        return ChatResponse(
            status_code=200,
            generated_text=generated_text,
        )
    except Exception as e:
        logger.error(f"ChatResponse Error : {str(e)}")
        return ChatResponse(
            status_code=500,
            error=str(e),
        )