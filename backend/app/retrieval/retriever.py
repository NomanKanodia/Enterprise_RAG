

# from app.embeddings.embedder import embed_query
# from app.schemas.retrieval import RetrievedChunk
# from app.vectorstore.faiss_store import FAISSStore


# class Retriever:

#     def __init__(
#         self,
#         vector_store: FAISSStore,
#         # similarity_threshold: float = 0.9
#     ):
#         self.vector_store = vector_store
#         self.similarity_threshold = similarity_threshold

#     def retrieve(
#         self,
#         query: str,
#         top_k: int = 3
#     ):

#         query_embedding = embed_query(
#             query
#         )

#         search_results = self.vector_store.search(
#             query_embedding,
#             top_k=top_k
#         )

#         results = []

#         for result in search_results:

#             chunk = result["chunk"]
#             distance = result["distance"]

#             # Lower L2 distance means greater similarity.
#             if distance >= self.similarity_threshold:
#                 continue

#             results.append(
#                 {
#                     "chunk": RetrievedChunk(
#                         document_id=chunk.document_id,
#                         page_number=chunk.page_number,
#                         chunk_number=chunk.chunk_number,
#                         text=chunk.text
#                     ),
#                     "distance": distance
#                 }
#             )

#         return results


from app.embeddings.embedder import embed_query
from app.vectorstore.faiss_store import FAISSStore


class Retriever:

    def __init__(
        self,
        vector_store: FAISSStore
    ):
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 3
    ):

        query_embedding = embed_query(
            query
        )

        return self.vector_store.search(
            query_embedding,
            top_k=top_k
        )