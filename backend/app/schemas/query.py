from pydantic import BaseModel

from app.schemas.retrieval import RetrievedChunk


class QueryRequest(BaseModel):
    query: str
    top_k: int = 3


class QueryResponse(BaseModel):
    query: str
    results: list[RetrievedChunk]