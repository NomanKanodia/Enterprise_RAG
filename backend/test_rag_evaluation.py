import json
from pathlib import Path

from app.services.rag_service import answer_query


QUESTIONS_FILE = Path(
    "evaluation/rag_questions.json"
)


def load_questions():
    with open(
        QUESTIONS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def check_answer(
    answer: str,
    expected_answer: str | None
):
    """
    Basic deterministic evaluation.

    For answerable questions we check that the
    generated answer is not empty.

    For unanswerable questions we check that
    the system explicitly says the information
    could not be found.
    """

    answer_lower = answer.lower()

    if expected_answer is None:

        return (
            "could not find the answer"
            in answer_lower
            or
            "could not find"
            in answer_lower
        )

    return len(
        answer.strip()
    ) > 0


def check_sources(
    sources,
    expected_document,
    expected_pages
):

    if expected_document is None:

        return len(sources) == 0

    for source in sources:

        if (
            source.get("document")
            == expected_document
            and
            source.get("page_number")
            in expected_pages
        ):
            return True

    return False


def main():

    questions = load_questions()

    answer_passes = 0
    source_passes = 0

    total = len(questions)

    print("\n")
    print("=" * 80)
    print("END-TO-END RAG EVALUATION")
    print("=" * 80)

    for question in questions:

        result = answer_query(
            question["question"]
        )

        answer = result["answer"]
        sources = result["sources"]

        answer_ok = check_answer(
            answer,
            question["expected_answer"]
        )

        source_ok = check_sources(
            sources,
            question["expected_document"],
            question["expected_pages"]
        )

        if answer_ok:
            answer_passes += 1

        if source_ok:
            source_passes += 1

        print("\n")
        print(
            f"Q{question['id']}: "
            f"{question['question']}"
        )

        print(
            f"Answer: {answer}"
        )

        print(
            f"Answer check: "
            f"{'PASS' if answer_ok else 'FAIL'}"
        )

        print(
            f"Sources: {sources}"
        )

        print(
            f"Source check: "
            f"{'PASS' if source_ok else 'FAIL'}"
        )

    answer_accuracy = (
        answer_passes / total
    ) * 100

    source_accuracy = (
        source_passes / total
    ) * 100

    print("\n")
    print("=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)

    print(
        f"Answer checks: "
        f"{answer_passes}/{total} "
        f"({answer_accuracy:.2f}%)"
    )

    print(
        f"Source checks: "
        f"{source_passes}/{total} "
        f"({source_accuracy:.2f}%)"
    )

    print("=" * 80)


if __name__ == "__main__":
    main()