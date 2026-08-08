from sentence_transformers import SentenceTransformer

from app.schemas.chunk import DocumentChunk
from app.schemas.embedding import EmbeddedChunk


model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_chunks(
    chunks: list[DocumentChunk]
) -> list[EmbeddedChunk]:

    if not chunks:
        return []

    texts = [chunk.text for chunk in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append(
            EmbeddedChunk(
                page_number=chunk.page_number,
                chunk_number=chunk.chunk_number,
                text=chunk.text,
                embedding=embedding.tolist()
            )
        )

    return embedded_chunks


def embed_query(query: str) -> list[float]:
    embedding = model.encode(query)

    return embedding.tolist()