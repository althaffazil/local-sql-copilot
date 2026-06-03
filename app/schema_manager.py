import duckdb

from app.config import DB_PATH


def delete_table(
    table_name: str
):

    conn = duckdb.connect(
        DB_PATH
    )

    tables = conn.execute(
        "SHOW TABLES"
    ).fetchall()

    existing_tables = [
        table[0]
        for table in tables
    ]

    if table_name not in existing_tables:

        conn.close()

        return {
            "success": False,
            "error": (
                f"Table '{table_name}' "
                "does not exist."
            )
        }

    conn.execute(
        f"DROP TABLE {table_name}"
    )

    conn.close()

    return {
        "success": True,
        "message": (
            f"Table '{table_name}' "
            "deleted successfully."
        )
    }