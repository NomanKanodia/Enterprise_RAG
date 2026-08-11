from pydantic import BaseModel


class DocumentChunk(BaseModel):
    document_id: str
    page_number: int
    chunk_number: int
    text: str