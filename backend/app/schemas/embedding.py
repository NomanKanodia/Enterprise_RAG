from pydantic import BaseModel


class EmbeddedChunk(BaseModel):
    page_number: int
    chunk_number: int
    text: str
    embedding: list[float]