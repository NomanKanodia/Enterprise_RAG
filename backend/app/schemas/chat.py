from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
    top_k: int = 3


class ChatSource(BaseModel):
    page_number: int


class ChatResponse(BaseModel):
    query: str
    answer: str
    sources: list[ChatSource]