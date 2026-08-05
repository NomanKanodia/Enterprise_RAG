from pathlib import Path

from app.schemas.document import PageContent
from app.document.parsers.pdf_parser import parse_pdf


def load_document(file_path: Path) -> list[PageContent]:
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return parse_pdf(file_path)

    raise ValueError(
        f"Unsupported document type: {extension}"
    )