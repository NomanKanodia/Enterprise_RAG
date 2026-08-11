import json
from pathlib import Path

from app.schemas.upload import DocumentMetadata


class DocumentStore:

    def __init__(
        self,
        directory: str = "vector_store"
    ):
        self.directory = Path(directory)
        self.directory.mkdir(
            parents=True,
            exist_ok=True
        )

        self.metadata_path = (
            self.directory / "documents.json"
        )

    def _load(self) -> dict:
        if not self.metadata_path.exists():
            return {}

        with open(
            self.metadata_path,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    def _save(self, documents: dict):
        with open(
            self.metadata_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                documents,
                file,
                indent=2
            )

    def add_document(
        self,
        document: DocumentMetadata
    ):
        documents = self._load()

        documents[document.document_id] = {
            "original_filename": document.original_filename,
            "stored_filename": document.stored_filename,
            "path": document.path
        }

        self._save(documents)

    def get_document(
        self,
        document_id: str
    ) -> dict | None:

        documents = self._load()

        return documents.get(
            document_id
        )