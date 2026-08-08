from pydantic import BaseModel


class RetrievedChunk(BaseModel):
    page_number: int
    chunk_number: int
    text: str