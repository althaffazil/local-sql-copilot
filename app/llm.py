from ollama import chat
from app.prompts import SQL_GENERATION_RULES
from ollama import chat
from app.sql_cleaner import extract_sql

def generate_sql(question: str, schema: str):

    prompt = f"""
{SQL_GENERATION_RULES}

Database Schema:

{schema}

User Question:
{question}
"""

    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    raw_response = response["message"]["content"]

    sql = extract_sql(raw_response)

    return sql

def repair_sql(
    original_sql: str,
    database_error: str,
    schema: str
):

    prompt = f"""
You are a DuckDB SQL expert.

Database Schema:

{schema}

Original SQL:

{original_sql}

Database Error:

{database_error}

Fix the SQL.

Rules:
- Return ONLY corrected SQL
- No explanations
- No markdown
- No comments
- Return executable DuckDB SQL
"""

    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    raw_response = response["message"]["content"]

    return extract_sql(raw_response)