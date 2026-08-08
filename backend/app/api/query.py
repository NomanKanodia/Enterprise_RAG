from fastapi import APIRouter

from app.schemas.query import QueryRequest, QueryResponse
from app.vectorstore.faiss_store import FAISSStore
from app.retrieval.retriever import Retriever


router = APIRouter()


@router.post(
    "/query",
    response_model=QueryResponse
)
async def query_documents(
    request: QueryRequest
):

    vector_store = FAISSStore.load()

    retriever = Retriever(
        vector_store
    )

    results = retriever.retrieve(
        request.query,
        top_k=request.top_k
    )

    return {
        "query": request.query,
        "results": results
    }