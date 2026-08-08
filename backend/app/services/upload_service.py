from pathlib import Path
from fastapi import UploadFile
import shutil
import uuid

from app.schemas.upload import DocumentMetadata
from app.document.loader import load_document
from app.chunking.langchain_chunker import chunk_document
from app.embeddings.embedder import embed_chunks
from app.vectorstore.faiss_store import FAISSStore

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

def process_upload(file: UploadFile):
    document = save_file(file)

    pages = load_document(
        Path(document.path)
    )
    
    chunks = chunk_document(pages)

    embedded_chunks = embed_chunks(chunks)
    vector_store = FAISSStore.load_or_create()

    vector_store.add_embeddings(
        embedded_chunks
    )

    vector_store.save()

    return {
        "document": document,
        "pages": pages,
        "chunks": chunks
    }
