from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
    top_k: int = 5


class Source(BaseModel):
    document: str
    page_number: int


class ChatResponse(BaseModel):
    query: str
    answer: str
    sources: list[Source]