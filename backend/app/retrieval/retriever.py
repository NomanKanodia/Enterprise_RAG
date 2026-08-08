from app.embeddings.embedder import embed_query
from app.schemas.retrieval import RetrievedChunk
from app.vectorstore.faiss_store import FAISSStore


class Retriever:

    def __init__(self, vector_store: FAISSStore):
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 3
    ) -> list[RetrievedChunk]:

        query_embedding = embed_query(query)

        embedded_chunks = self.vector_store.search(
            query_embedding,
            top_k=top_k
        )

        results = []

        for chunk in embedded_chunks:
            results.append(
                RetrievedChunk(
                    page_number=chunk.page_number,
                    chunk_number=chunk.chunk_number,
                    text=chunk.text
                )
            )

        return results