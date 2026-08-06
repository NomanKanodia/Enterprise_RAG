from pydantic import BaseModel
from app.schemas.upload import DocumentMetadata
from app.schemas.chunk import DocumentChunk

class PageContent(BaseModel):
    page_number: int
    text: str

class DocumentProcessingResponse(BaseModel):
    message: str
    document: DocumentMetadata
    pages: list[PageContent]
    chunks: list[DocumentChunk]  