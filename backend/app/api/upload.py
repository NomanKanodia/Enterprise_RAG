from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.upload_service import save_file
from app.schemas.upload import UploadResponse

router = APIRouter()

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

@router.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_file(file: UploadFile = File(...)):
    extension = "." + file.filename.split(".")[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Only PDF, DOCX and TXT are allowed."
        )

    saved_file = save_file(file)

    return {
        "message": "File uploaded successfully",
        "file": saved_file
    }