# from app.generation.llm import generate_answer
# from app.retrieval.retriever import Retriever
# from app.vectorstore.faiss_store import FAISSStore
# from app.vectorstore.document_store import DocumentStore


# def answer_query(
#     query: str,
#     top_k: int = 3
# ):

#     # Load the persistent vector store
#     vector_store = FAISSStore.load()

#     # Create retriever
#     retriever = Retriever(
#         vector_store
#     )

#     # Retrieve relevant chunks
#     retrieved_chunks = retriever.retrieve(
#         query,
#         top_k=top_k
#     )

#     # No relevant information found
#     if not retrieved_chunks:
#         return {
#             "answer": (
#                 "I could not find the answer "
#                 "in the uploaded documents."
#             ),
#             "sources": []
#         }

#     # Load document metadata
#     document_store = DocumentStore()

#     # Build context for the LLM
#     context_parts = []

#     for chunk in retrieved_chunks:

#         context_parts.append(
#             f"[Document ID: {chunk.document_id} | "
#             f"Page {chunk.page_number}]\n"
#             f"{chunk.text}"
#         )

#     context = "\n\n".join(context_parts)

#     # Build RAG prompt
#     prompt = f"""
# You are an enterprise document assistant.

# Answer the user's question using ONLY the information
# provided in the context below.

# If the answer cannot be found in the context,
# say that you could not find the answer in the uploaded documents.

# Do not use outside knowledge.
# Do not make up information.

# Context:
# --------------------
# {context}
# --------------------

# User Question:
# {query}

# Answer:
# """

#     # Generate answer
#     answer = generate_answer(
#         prompt
#     )

#     # Build unique sources
#     sources = []
#     seen_sources = set()

#     for chunk in retrieved_chunks:

#         document = document_store.get_document(
#             chunk.document_id
#         )

#         if document is None:
#             continue

#         source_key = (
#             chunk.document_id,
#             chunk.page_number
#         )

#         # Avoid duplicate document + page combinations
#         if source_key in seen_sources:
#             continue

#         seen_sources.add(source_key)

#         sources.append(
#             {
#                 "document": document["original_filename"],
#                 "page_number": chunk.page_number
#             }
#         )

#     return {
#         "answer": answer,
#         "sources": sources
#     }




from app.generation.llm import generate_answer
from app.retrieval.retriever import Retriever
from app.vectorstore.faiss_store import FAISSStore
from app.vectorstore.document_store import DocumentStore


def answer_query(
    query: str,
    top_k: int = 5
):

    # Load the persistent vector store
    vector_store = FAISSStore.load()

    # Create retriever
    retriever = Retriever(
        vector_store
    )

    # Retrieve relevant chunks
    retrieval_results = retriever.retrieve(
        query,
        top_k=top_k
    )

    # No sufficiently relevant information found
    if not retrieval_results:
        return {
            "answer": (
                "I could not find the answer "
                "in the uploaded documents."
            ),
            "sources": []
        }

    # Load document metadata
    document_store = DocumentStore()

    # Build context
    context_parts = []

    for result in retrieval_results:

        chunk = result["chunk"]

        context_parts.append(
            f"[Document ID: {chunk.document_id} | "
            f"Page {chunk.page_number}]\n"
            f"{chunk.text}"
        )

    context = "\n\n".join(
        context_parts
    )

    # Build RAG prompt
    prompt = f"""
You are an enterprise document assistant.

Your task is to answer the user's question using ONLY the
information explicitly provided in the context.

IMPORTANT RULES:

1. Do not use outside knowledge.
2. Do not invent or assume information.
3. If the answer is present in the context, answer it directly.
4. Preserve important factual details from the context, especially:
   - names of organizations or companies
   - eligibility and scope statements
   - dates
   - percentages
   - monetary amounts
   - distances
   - durations
   - limits
   - names of cities, people, or categories
5. If the question asks "who", identify the exact people,
   employees, organization, or category stated in the context.
6. If the question asks "how many", "how much", "what percentage",
   "how long", or "when", include the exact value from the context.
7. Do not replace a specific statement with a vague generalization.
8. If multiple pieces of information are required to answer the
   question, include all relevant pieces supported by the context.
9. If the answer cannot be found in the context, respond exactly:
   "I could not find the answer in the uploaded documents."
10. Do not mention information that is not supported by the context.

## Context

{context}

## User Question

{query}

## Answer
"""

    # Generate answer
    answer = generate_answer(
        prompt
    )

    # Build unique sources
    sources = []
    seen_sources = set()

    for result in retrieval_results:

        chunk = result["chunk"]

        document = document_store.get_document(
            chunk.document_id
        )

        if document is None:
            continue

        source_key = (
            chunk.document_id,
            chunk.page_number
        )

        if source_key in seen_sources:
            continue

        seen_sources.add(
            source_key
        )

        sources.append(
            {
                "document": document["original_filename"],
                "page_number": chunk.page_number
            }
        )

    return {
        "answer": answer,
        "sources": sources
    }