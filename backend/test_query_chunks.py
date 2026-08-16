from app.embeddings.embedder import embed_query
from app.vectorstore.faiss_store import FAISSStore


query = "When did the Travel Policy come into effect?"

vector_store = FAISSStore.load()

query_embedding = embed_query(query)

results = vector_store.search(
    query_embedding,
    top_k=5
)

print("\n")
print("=" * 80)
print("RETRIEVAL DEBUG")
print("=" * 80)

for rank, result in enumerate(results, start=1):

    chunk = result["chunk"]
    distance = result["distance"]

    print("\n")
    print(f"Rank: {rank}")
    print(f"Distance: {distance:.4f}")
    print(f"Document ID: {chunk.document_id}")
    print(f"Page: {chunk.page_number}")
    print("-" * 80)
    print(chunk.text)