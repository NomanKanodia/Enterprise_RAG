from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.upload_service import process_upload
from app.schemas.document import DocumentProcessingResponse

router = APIRouter()

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

@router.post(
    "/upload",
    response_model=DocumentProcessingResponse
)
async def upload_file(file: UploadFile = File(...)):
    extension = "." + file.filename.split(".")[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Only PDF, DOCX and TXT are allowed."
        )

    result = process_upload(file)

    return {
        "message": "File uploaded successfully",
        "document": result["document"],
        "pages": result["pages"]
    }