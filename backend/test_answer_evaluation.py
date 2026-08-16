import json
from pathlib import Path


CHECKS_FILE = Path(
    "evaluation/answer_checks.json"
)


# Answers successfully generated during our
# previous RAG evaluation.
#
# Q13 is intentionally omitted because the
# Gemini quota was exhausted before it was
# successfully generated.
GENERATED_ANSWERS = {
    1: """
    Based on the provided document, the objectives of the Travel Policy are:

    To maintain the image of the company and to have uniform expense reimbursement
    for categorized employees on official travel.

    To lay down the Band / Grade-wise entitlements of various expenses incurred
    by employees while traveling on official/business work.

    To ensure expenses are cost-effective and economical in optimizing productivity.
    """,

    2: """
    Based on the provided documents, eligibility under the Travel Policy applies to:

    Categorized employees traveling on official or business work.

    Employees based on their job levels, specifically their Job band and grade.

    All Non-Sales Employees.
    """,

    3: """
    An employee can claim 25% of their eligible amount when staying at a relative
    or friend's home or room.
    """,

    4: """
    Based on the provided context, for twin sharing, the maximum claim that can
    be made is 125% of the eligible amount of the Senior level employee.
    """,

    5: """
    Based on the provided documents, travelling advance must be settled within
    2 days after the tour programme.
    """,

    6: """
    In case of not getting bills in remote areas, the employee can claim the
    eligible amount by self-attestation.
    """,

    7: """
    No. According to the provided documents, Boarding & Lodging cannot be claimed
    as a combined limit.
    """,

    8: """
    Based on the provided documents, the cities classified as metros are:

    Mumbai
    Delhi
    Kolkata
    """,

    9: """
    Based on the provided context, non-sales employees are eligible for food
    reimbursement during out-of-office work when they spend more than 6 hours
    on that work.
    """,

    10: """
    Based on the provided documents, the maximum distance for official travel
    by personal bike is 50 kms on any day.
    """,

    11: """
    Based on the provided context, group travel beyond 200 km by personal car
    requires 3 or more people.
    """,

    12: """
    Based on the provided documents, no, driver charges are not paid for
    official travel using a personal car.
    """
}


def load_checks():

    with open(
        CHECKS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def normalize(text: str) -> str:

    text = text.lower()

    replacements = {
        "-": " ",
        "–": " ",
        "—": " ",
        "_": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Normalize repeated whitespace.
    return " ".join(text.split())


def contains_all(
    answer: str,
    terms: list[str]
) -> bool:

    return all(
        normalize(term) in answer
        for term in terms
    )


def contains_any_group(
    answer: str,
    groups: list[list[str]]
) -> bool:

    for group in groups:

        if contains_all(
            answer,
            group
        ):
            return True

    return False


def evaluate_answer(
    answer: str,
    check: dict
) -> tuple[str, list[str]]:

    normalized_answer = normalize(
        answer
    )

    missing = []

    # -----------------------------------------
    # Required ALL
    # -----------------------------------------

    for group in check.get(
        "required_all",
        []
    ):

        if not contains_all(
            normalized_answer,
            group
        ):

            missing.append(
                " AND ".join(group)
            )

    # -----------------------------------------
    # Required ANY
    # -----------------------------------------

    required_any = check.get(
        "required_any",
        []
    )

    if required_any:

        if not contains_any_group(
            normalized_answer,
            required_any
        ):

            alternatives = [
                " + ".join(group)
                for group in required_any
            ]

            missing.append(
                "one of: "
                + " OR ".join(alternatives)
            )

    # -----------------------------------------
    # Final status
    # -----------------------------------------

    if missing:

        return "FAIL", missing

    return "PASS", []


def main():

    checks = load_checks()

    passed = 0
    failed = 0
    not_evaluated = 0

    print("\n")
    print("=" * 80)
    print("LOCAL RAG ANSWER EVALUATION")
    print("=" * 80)

    for check in checks:

        question_id = check["id"]

        answer = GENERATED_ANSWERS.get(
            question_id
        )

        print(
            f"\nQ{question_id}"
        )

        # -----------------------------------------
        # Not evaluated
        # -----------------------------------------

        if answer is None:

            not_evaluated += 1

            print(
                "    Status: NOT_EVALUATED"
            )

            print(
                "    Reason: No successful LLM "
                "generation was available."
            )

            continue

        # -----------------------------------------
        # Evaluate
        # -----------------------------------------

        status, missing = evaluate_answer(
            answer,
            check
        )

        if status == "PASS":

            passed += 1

        else:

            failed += 1

        print(
            f"    Status: {status}"
        )

        if missing:

            print(
                "    Missing facts:"
            )

            for item in missing:

                print(
                    f"      - {item}"
                )

    evaluated = passed + failed

    print("\n")
    print("=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)

    print(
        f"Passed: {passed}"
    )

    print(
        f"Failed: {failed}"
    )

    print(
        f"Not evaluated: {not_evaluated}"
    )

    print(
        f"Evaluated questions: {evaluated}"
    )

    if evaluated > 0:

        accuracy = (
            passed / evaluated
        ) * 100

        print(
            f"Answer correctness: "
            f"{passed}/{evaluated} "
            f"({accuracy:.2f}%)"
        )

    print("=" * 80)


if __name__ == "__main__":
    main()