from pathlib import Path
from fastapi import UploadFile
from app.schemas.upload import DocumentMetadata
import shutil
import uuid

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def save_file(file: UploadFile) -> DocumentMetadata:
    extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{extension}"

    file_path = UPLOAD_DIR / unique_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return DocumentMetadata (
        original_filename=file.filename,
        stored_filename=unique_filename,
        path=str(file_path)
    )