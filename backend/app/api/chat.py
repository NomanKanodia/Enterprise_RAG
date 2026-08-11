from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import answer_query


router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(
    request: ChatRequest
):
    result = answer_query(
        query=request.query,
        top_k=request.top_k
    )

    return {
        "query": request.query,
        "answer": result["answer"],
        "sources": result["sources"]
    }