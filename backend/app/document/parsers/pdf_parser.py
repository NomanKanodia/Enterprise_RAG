import fitz
from pathlib import Path

from app.schemas.document import PageContent


def parse_pdf(file_path: Path) -> list[PageContent]:
    pages = []

    with fitz.open(file_path) as document:
        for page_number, page in enumerate(document, start=1):
            pages.append(
                PageContent(
                    page_number=page_number,
                    text=page.get_text()
                )
            )

    return pages