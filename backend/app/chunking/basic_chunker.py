from app.schemas.document import PageContent
from app.schemas.chunk import DocumentChunk


def chunk_document(
    pages: list[PageContent],
    chunk_size: int = 500,
    overlap: int = 100
) -> list[DocumentChunk]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    chunk_number = 1

    for page in pages:

        text = page.text.strip()

        if not text:
            continue

        start = 0

        while start < len(text):

            end = min(start + chunk_size, len(text))

            split_point = text.rfind(" ", start, end)

            if split_point == -1 or split_point <= start:
                split_point = end

            chunk_text = text[start:split_point].strip()

            if chunk_text:
                chunks.append(
                    DocumentChunk(
                        page_number=page.page_number,
                        chunk_number=chunk_number,
                        text=chunk_text
                    )
                )

                chunk_number += 1

            if split_point >= len(text):
                break

            next_start = max(0, split_point - overlap)

            if next_start <= start:
                next_start = split_point

            start = next_start

    return chunks