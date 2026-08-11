from pydantic import BaseModel


class EmbeddedChunk(BaseModel):
    document_id: str
    page_number: int
    chunk_number: int
    text: str
    embedding: list[float]