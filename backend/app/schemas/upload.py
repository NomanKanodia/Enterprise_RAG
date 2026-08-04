from pydantic import BaseModel


class DocumentMetadata(BaseModel):
    original_filename: str
    stored_filename: str
    path: str


class UploadResponse(BaseModel):
    message: str
    file: DocumentMetadata