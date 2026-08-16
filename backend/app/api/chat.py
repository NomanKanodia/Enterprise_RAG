from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import answer_query


router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):

    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty."
        )

    if request.top_k < 1:
        raise HTTPException(
            status_code=400,
            detail="top_k must be at least 1."
        )

    try:
        result = answer_query(
            query=request.query,
            top_k=request.top_k
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail="Failed to process the query."
        ) from exc

    return {
        "query": request.query,
        "answer": result["answer"],
        "sources": result["sources"]
    }