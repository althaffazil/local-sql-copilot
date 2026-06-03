READ_ONLY_BLOCKED_WORDS = [
    "delete",
    "drop",
    "truncate",
    "update",
    "insert",
    "alter",
    "create",
    "remove",
    "replace",
    "merge"
]


def check_question_policy(question: str):

    question_lower = question.lower()

    for word in READ_ONLY_BLOCKED_WORDS:

        if word in question_lower:

            return (
                False,
                f"Read-only mode enabled. Operation '{word}' is not allowed."
            )

    return (
        True,
        None
    )