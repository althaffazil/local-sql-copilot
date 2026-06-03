import re


def extract_sql(text: str):

    text = text.strip()

    # Remove markdown blocks
    text = text.replace("```sql", "")
    text = text.replace("```", "")

    sql_keywords = [
        "SELECT",
        "WITH",
        "INSERT",
        "UPDATE",
        "DELETE"
    ]

    lines = text.splitlines()

    start_idx = None

    for i, line in enumerate(lines):
        upper = line.strip().upper()

        if any(upper.startswith(k) for k in sql_keywords):
            start_idx = i
            break

    if start_idx is None:
        return text

    sql = "\n".join(lines[start_idx:])

    match = re.search(r";", sql)

    if match:
        sql = sql[:match.end()]

    return sql.strip()