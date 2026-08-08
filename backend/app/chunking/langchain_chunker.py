from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.schemas.chunk import DocumentChunk
from app.schemas.document import PageContent


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=[
        "\n\n",
        "\n",
        " ",
        ""
    ]
)


def chunk_document(
    pages: list[PageContent]
) -> list[DocumentChunk]:

    chunks = []
    chunk_number = 1

    for page in pages:

        page_chunks = text_splitter.split_text(page.text)

        for chunk in page_chunks:

            chunks.append(
                DocumentChunk(
                    page_number=page.page_number,
                    chunk_number=chunk_number,
                    text=chunk
                )
            )

            chunk_number += 1

    return chunks