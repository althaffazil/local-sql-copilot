import re


ALLOWED_STARTS = [
    "SELECT",
    "WITH"
]


def validate_sql(sql: str):

    if not sql:
        return False, "Empty SQL generated"

    sql = sql.strip()

    sql_upper = sql.upper()

    if not any(
        sql_upper.startswith(keyword)
        for keyword in ALLOWED_STARTS
    ):
        return (
            False,
            f"Only SELECT and WITH statements are allowed. Generated SQL starts with: {sql.split()[0]}"
        )

    dangerous_keywords = [
        "DROP",
        "DELETE",
        "TRUNCATE",
        "ALTER",
        "UPDATE",
        "INSERT",
        "CREATE",
        "REPLACE",
        "MERGE"
    ]

    for keyword in dangerous_keywords:

        pattern = rf"\b{keyword}\b"

        if re.search(pattern, sql_upper):
            return (
                False,
                f"Dangerous keyword detected: {keyword}"
            )

    return True, None