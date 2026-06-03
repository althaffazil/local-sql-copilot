from ollama import chat


def classify_question(
    question: str
) -> bool:

    prompt = f"""
You are a classifier.

Determine whether the user's question
is intended to retrieve information
from a database.

Respond with ONLY:

DATABASE

or

NON_DATABASE

Examples:

Question:
Show all customers

DATABASE

Question:
Average salary by department

DATABASE

Question:
Tell me a joke

NON_DATABASE

Question:
What is life

NON_DATABASE

Question:
Who won IPL 2025

NON_DATABASE

User Question:
{question}
"""

    try:

        response = chat(
            model="qwen3:4b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = (
            response["message"]["content"]
            .strip()
            .upper()
        )

        return answer == "DATABASE"

    except Exception:

        return False