import json
from pathlib import Path

from app.embeddings.embedder import embed_query
from app.vectorstore.faiss_store import FAISSStore


QUESTIONS_FILE = Path("evaluation/questions.json")
DOCUMENTS_FILE = Path("vector_store/documents.json")

TOP_K = 3


def load_questions():
    with open(
        QUESTIONS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def load_document_mapping():
    """
    Create a mapping:

        original_filename -> document_id
    """

    with open(
        DOCUMENTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        documents = json.load(file)

    filename_to_id = {}

    for document_id, metadata in documents.items():

        filename = metadata["original_filename"]

        filename_to_id[filename] = document_id

    return filename_to_id


def evaluate_question(
    question,
    vector_store,
    filename_to_id
):
    query = question["question"]

    query_embedding = embed_query(
        query
    )

    results = vector_store.search(
        query_embedding,
        top_k=TOP_K
    )

    expected_document = question[
        "expected_document"
    ]

    expected_pages = set(
        question["expected_pages"]
    )

    # ------------------------------------------------
    # Unanswerable question
    # ------------------------------------------------

    if expected_document is None:

        # For an unanswerable question, we don't
        # expect a correct document/page.

        return {
            "answerable": False,
            "retrieval_hit": None,
            "results": results
        }

    # ------------------------------------------------
    # Get expected document ID
    # ------------------------------------------------

    expected_document_id = filename_to_id.get(
        expected_document
    )

    if expected_document_id is None:

        raise ValueError(
            f"Document '{expected_document}' "
            f"was not found in documents.json"
        )

    # ------------------------------------------------
    # Check whether correct document + page
    # appears in top-k
    # ------------------------------------------------

    retrieval_hit = False

    for result in results:

        chunk = result["chunk"]

        if (
            chunk.document_id == expected_document_id
            and chunk.page_number in expected_pages
        ):
            retrieval_hit = True
            break

    return {
        "answerable": True,
        "retrieval_hit": retrieval_hit,
        "results": results
    }


def main():

    questions = load_questions()

    filename_to_id = load_document_mapping()

    vector_store = FAISSStore.load()

    answerable_questions = 0
    retrieval_hits = 0

    unanswerable_questions = 0

    print("\n")
    print("=" * 80)
    print("RAG RETRIEVAL BASELINE EVALUATION")
    print("=" * 80)

    print(
        f"Top-K: {TOP_K}"
    )

    print(
        "Threshold filtering: DISABLED"
    )

    print("=" * 80)

    for question in questions:

        result = evaluate_question(
            question,
            vector_store,
            filename_to_id
        )

        results = result["results"]

        # --------------------------------------------
        # Answerable question
        # --------------------------------------------

        if result["answerable"]:

            answerable_questions += 1

            if result["retrieval_hit"]:
                retrieval_hits += 1

            status = (
                "PASS"
                if result["retrieval_hit"]
                else "FAIL"
            )

            print(
                f"\n[{status}] "
                f"Q{question['id']}: "
                f"{question['question']}"
            )

            print(
                f"    Expected document: "
                f"{question['expected_document']}"
            )

            print(
                f"    Expected pages: "
                f"{question['expected_pages']}"
            )

        # --------------------------------------------
        # Unanswerable question
        # --------------------------------------------

        else:

            unanswerable_questions += 1

            print(
                f"\n[UNANSWERABLE] "
                f"Q{question['id']}: "
                f"{question['question']}"
            )

        # --------------------------------------------
        # Show retrieved results
        # --------------------------------------------

        for rank, retrieved in enumerate(
            results,
            start=1
        ):

            chunk = retrieved["chunk"]
            distance = retrieved["distance"]

            print(
                f"    #{rank} "
                f"distance={distance:.4f} "
                f"document_id={chunk.document_id} "
                f"page={chunk.page_number}"
            )

    # -----------------------------------------------
    # Final metrics
    # -----------------------------------------------

    if answerable_questions > 0:

        hit_at_k = (
            retrieval_hits /
            answerable_questions
        ) * 100

    else:
        hit_at_k = 0.0

    print("\n")
    print("=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)

    print(
        f"Answerable questions: "
        f"{answerable_questions}"
    )

    print(
        f"Raw Hit@{TOP_K}: "
        f"{retrieval_hits}/"
        f"{answerable_questions} "
        f"({hit_at_k:.2f}%)"
    )

    print(
        f"Unanswerable questions: "
        f"{unanswerable_questions}"
    )

    print("=" * 80)


if __name__ == "__main__":
    main()