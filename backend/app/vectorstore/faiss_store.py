import pickle
from pathlib import Path

import faiss
import numpy as np

from app.schemas.embedding import EmbeddedChunk


class FAISSStore:

    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.chunks: list[EmbeddedChunk] = []

    def add_embeddings(
        self,
        embedded_chunks: list[EmbeddedChunk]
    ):
        if not embedded_chunks:
            return

        vectors = np.array(
            [chunk.embedding for chunk in embedded_chunks],
            dtype="float32"
        )

        self.index.add(vectors)

        self.chunks.extend(embedded_chunks)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 3
    ) -> list[EmbeddedChunk]:

        if self.index.ntotal == 0:
            return []

        query_vector = np.array(
            [query_embedding],
            dtype="float32"
        )

        distances, indices = self.index.search(
            query_vector,
            min(top_k, self.index.ntotal)
        )

        results = []

        for index in indices[0]:
            if index != -1:
                results.append(self.chunks[index])

        return results

    def save(
        self,
        directory: str = "vector_store"
    ):
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)

        faiss.write_index(
            self.index,
            str(path / "index.faiss")
        )

        with open(path / "chunks.pkl", "wb") as file:
            pickle.dump(self.chunks, file)

    @classmethod
    def load(
        cls,
        directory: str = "vector_store",
        dimension: int = 384
    ):
        path = Path(directory)

        index_path = path / "index.faiss"
        chunks_path = path / "chunks.pkl"

        store = cls(dimension)

        store.index = faiss.read_index(
            str(index_path)
        )

        with open(chunks_path, "rb") as file:
            store.chunks = pickle.load(file)

        return store

    @classmethod
    def load_or_create(
        cls,
        directory: str = "vector_store",
        dimension: int = 384
    ):
        path = Path(directory)

        index_path = path / "index.faiss"
        chunks_path = path / "chunks.pkl"

        if index_path.exists() and chunks_path.exists():
            return cls.load(
                directory,
                dimension
            )

        return cls(dimension)