import duckdb

from app.config import DB_PATH


def get_database_schema():

    conn = duckdb.connect(DB_PATH)

    tables = conn.execute(
        "SHOW TABLES"
    ).fetchall()

    schema_sections = []

    for table in tables:

        table_name = table[0]

        columns = conn.execute(
            f"DESCRIBE {table_name}"
        ).fetchall()

        schema_text = f"{table_name}(\n"

        column_lines = []

        for column in columns:

            column_name = column[0]
            column_type = column[1]

            column_lines.append(
                f"    {column_name} {column_type}"
            )

        schema_text += ",\n".join(
            column_lines
        )

        schema_text += "\n)\n"

        schema_sections.append(
            schema_text
        )

    conn.close()

    return "\n".join(
        schema_sections
    )


def get_schema_json():

    conn = duckdb.connect(
        DB_PATH
    )

    tables = conn.execute(
        "SHOW TABLES"
    ).fetchall()

    result = []

    for table in tables:

        table_name = table[0]

        columns = conn.execute(
            f"DESCRIBE {table_name}"
        ).fetchall()

        result.append(
            {
                "table": table_name,
                "columns": [
                    {
                        "name": c[0],
                        "type": c[1]
                    }
                    for c in columns
                ]
            }
        )

    conn.close()

    return result