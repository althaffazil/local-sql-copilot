from app.llm import (
    generate_sql,
    repair_sql
)

from app.database import (
    execute_query
)

from app.sql_validator import (
    validate_sql
)

from app.policy import (
    check_question_policy
)

from app.schema import (
    get_database_schema
)

from app.export_store import (
    save_result
)

from app.question_guard import (
    classify_question
)

MAX_RETRIES = 3


def get_confidence(
    repair_count: int
):

    if repair_count == 0:
        return "HIGH"

    if repair_count == 1:
        return "MEDIUM"

    return "LOW"


def references_schema_tables(
    sql: str,
    schema: str
):

    sql_lower = sql.lower()

    lines = schema.splitlines()

    table_names = []

    for line in lines:

        line = line.strip()

        if "(" in line:

            table_name = (
                line.split("(")[0]
                .strip()
            )

            if table_name:

                table_names.append(
                    table_name.lower()
                )

    for table_name in table_names:

        if table_name in sql_lower:

            return True

    return False


def process_question(
    question: str
):

    allowed, policy_error = (
        check_question_policy(
            question
        )
    )

    if not allowed:

        return {
            "success": False,
            "question": question,
            "error": policy_error,
            "original_sql": "",
            "final_sql": "",
            "repair_count": 0,
            "confidence": "HIGH",
            "attempts": []
        }

    if not classify_question(
        question
    ):

        return {
            "success": False,
            "question": question,
            "error": (
                "This question does not "
                "appear to be related to "
                "the current database."
            ),
            "original_sql": "",
            "final_sql": "",
            "repair_count": 0,
            "confidence": "LOW",
            "attempts": []
        }

    schema = get_database_schema()

    attempts = []

    original_sql = generate_sql(
        question,
        schema
    )

    if not references_schema_tables(
        original_sql,
        schema
    ):

        return {
            "success": False,
            "question": question,
            "error": (
                "Generated SQL does not "
                "reference any table in "
                "the current schema."
            ),
            "original_sql": original_sql,
            "final_sql": original_sql,
            "repair_count": 0,
            "confidence": "LOW",
            "attempts": []
        }

    current_sql = original_sql

    for retry_count in range(
        MAX_RETRIES + 1
    ):

        is_valid, validation_error = (
            validate_sql(
                current_sql
            )
        )

        if not is_valid:

            return {
                "success": False,
                "question": question,
                "error": validation_error,
                "original_sql": original_sql,
                "final_sql": current_sql,
                "repair_count": retry_count,
                "confidence": get_confidence(
                    retry_count
                ),
                "attempts": attempts
            }

        result = execute_query(
            current_sql
        )

        if result["success"]:

            save_result(
                result
            )

            return {
                "success": True,
                "question": question,
                "schema": schema,
                "original_sql": original_sql,
                "final_sql": current_sql,
                "repair_count": retry_count,
                "confidence": get_confidence(
                    retry_count
                ),
                "attempts": attempts,
                "result": result
            }

        attempts.append(
            {
                "attempt":
                    retry_count + 1,
                "sql":
                    current_sql,
                "error":
                    result["error"]
            }
        )

        if retry_count >= MAX_RETRIES:

            return {
                "success": False,
                "question": question,
                "error": result["error"],
                "original_sql": original_sql,
                "final_sql": current_sql,
                "repair_count": retry_count,
                "confidence": get_confidence(
                    retry_count
                ),
                "attempts": attempts
            }

        current_sql = repair_sql(
            original_sql=current_sql,
            database_error=result[
                "error"
            ],
            schema=schema
        )

    return {
        "success": False,
        "question": question,
        "error":
            "Unknown error occurred",
        "original_sql":
            original_sql,
        "final_sql":
            current_sql,
        "repair_count":
            MAX_RETRIES,
        "confidence":
            "LOW",
        "attempts":
            attempts
    }