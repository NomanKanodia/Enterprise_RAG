from app.generation.llm import generate_answer
from app.retrieval.retriever import Retriever
from app.vectorstore.faiss_store import FAISSStore


def answer_query(
    query: str,
    top_k: int = 3
):

    vector_store = FAISSStore.load()

    retriever = Retriever(
        vector_store
    )

    retrieved_chunks = retriever.retrieve(
        query,
        top_k=top_k
    )

    if not retrieved_chunks:
        return {
            "answer": (
                "I could not find the answer "
                "in the uploaded documents."
            ),
            "sources": []
        }

    context_parts = []

    for chunk in retrieved_chunks:
        context_parts.append(
            f"[Page {chunk.page_number}]\n"
            f"{chunk.text}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are an enterprise document assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context,
say that you could not find the answer in the uploaded documents.

Do not use outside knowledge.
Do not make up information.

Context:
--------------------
{context}
--------------------

User Question:
{query}

Answer:
"""

    answer = generate_answer(
        prompt
    )

    source_pages = sorted(
        set(
            chunk.page_number
            for chunk in retrieved_chunks
        )
    )

    sources = [
        {
            "page_number": page_number
        }
        for page_number in source_pages
    ]

    return {
        "answer": answer,
        "sources": sources
    }