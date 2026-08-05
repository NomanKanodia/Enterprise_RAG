from pydantic import BaseModel
from app.schemas.upload import DocumentMetadata

class PageContent(BaseModel):
    page_number: int
    text: str

class DocumentProcessingResponse(BaseModel):
    message: str
    document: DocumentMetadata
    pages: list[PageContent]    