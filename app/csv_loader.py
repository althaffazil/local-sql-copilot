import os
import pandas as pd
import duckdb

from app.config import DB_PATH


UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


def load_csv_to_duckdb(file_path: str):

    file_name = os.path.basename(
        file_path
    )

    table_name = (
        os.path.splitext(file_name)[0]
        .lower()
        .replace(" ", "_")
    )

    df = pd.read_csv(
        file_path
    )

    conn = duckdb.connect(
        DB_PATH
    )

    conn.register(
        "temp_df",
        df
    )

    conn.execute(
        f"""
        CREATE OR REPLACE TABLE
        {table_name}
        AS
        SELECT *
        FROM temp_df
        """
    )

    conn.close()

    return {
        "table_name": table_name,
        "rows": len(df),
        "columns": list(df.columns)
    }