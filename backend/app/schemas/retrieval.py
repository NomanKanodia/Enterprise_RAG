from pydantic import BaseModel


class RetrievedChunk(BaseModel):
    document_id: str
    page_number: int
    chunk_number: int
    text: str