from fastapi import APIRouter, HTTPException

from app.schemas.query import QueryRequest, QueryResponse
from app.vectorstore.faiss_store import FAISSStore
from app.retrieval.retriever import Retriever


router = APIRouter()


@router.post(
    "/query",
    response_model=QueryResponse
)
async def query_documents(request: QueryRequest):

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
        vector_store = FAISSStore.load()
    except Exception as exc:
        raise HTTPException(
            status_code=404,
            detail="No vector store found. Upload a document first."
        ) from exc

    retriever = Retriever(vector_store)

    raw_results = retriever.retrieve(
        request.query,
        top_k=request.top_k
    )

    results = []

    for item in raw_results:
        chunk = item["chunk"]

        results.append({
            "document_id": chunk.document_id,
            "page_number": chunk.page_number,
            "chunk_number": chunk.chunk_number,
            "text": chunk.text,
            "distance": item["distance"]
        })

    return {
        "query": request.query,
        "results": results
    }