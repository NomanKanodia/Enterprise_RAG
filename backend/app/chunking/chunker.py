from app.schemas.document import PageContent
from app.schemas.chunk import DocumentChunk


def chunk_document(
    pages: list[PageContent],
    chunk_size: int = 500
) -> list[DocumentChunk]:

    chunks = []

    chunk_number = 1

    for page in pages:

        text = page.text

        for start in range(0, len(text), chunk_size):

            chunk_text = text[start:start + chunk_size]

            chunks.append(
                DocumentChunk(
                    page_number=page.page_number,
                    chunk_number=chunk_number,
                    text=chunk_text
                )
            )

            chunk_number += 1

    return chunks