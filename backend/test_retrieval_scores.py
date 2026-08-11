from app.embeddings.embedder import embed_query
from app.vectorstore.faiss_store import FAISSStore


vector_store = FAISSStore.load()


queries = [
    "What is the company's annual leave policy?",
    "What percentage of the eligible lodging amount can an employee claim when staying at a relative or friend's home?"
]


for query in queries:

    print("\n" + "=" * 70)
    print("QUERY:", query)
    print("=" * 70)

    query_embedding = embed_query(query)

    results = vector_store.search(
        query_embedding,
        top_k=5
    )

    for result in results:

        chunk = result["chunk"]
        distance = result["distance"]

        print(f"\nDistance: {distance:.4f}")
        print(f"Document ID: {chunk.document_id}")
        print(f"Page: {chunk.page_number}")
        print(f"Text: {chunk.text[:300]}")