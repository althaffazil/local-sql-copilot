from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File

from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

from app.query_engine import process_question
from app.csv_loader import load_csv_to_duckdb
from app.schema import get_schema_json
from fastapi.responses import FileResponse
from app.schema_manager import (
    delete_table
)
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import pandas as pd
import os

from app.export_store import get_last_result

app = FastAPI(
    title="Local SQL Copilot"
)

app.mount(
    "/static",
    StaticFiles(
        directory="app/static"
    ),
    name="static"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str

@app.get("/")
def dashboard():

    return FileResponse(
        "app/static/dashboard.html"
    )


@app.get("/schema")
def schema():

    return {
        "tables": get_schema_json()
    }


@app.post("/query")
def query_database(
    request: QueryRequest
):

    return process_question(
        request.question
    )


@app.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...)
):

    file_path = (
        f"uploads/{file.filename}"
    )

    contents = await file.read()

    with open(
        file_path,
        "wb"
    ) as f:

        f.write(contents)

    result = load_csv_to_duckdb(
        file_path
    )

    return {
        "success": True,
        "message": "CSV uploaded successfully",
        "table": result
    }

@app.get("/export/csv")
def export_csv():

    result = get_last_result()

    if not result:

        return {
            "success": False,
            "error": "No query results available"
        }

    df = pd.DataFrame(
        result["rows"],
        columns=result["columns"]
    )

    output_file = "exports/query_results.csv"

    os.makedirs(
        "exports",
        exist_ok=True
    )

    df.to_csv(
        output_file,
        index=False
    )

    return FileResponse(
        output_file,
        filename="query_results.csv",
        media_type="text/csv"
    )

@app.get("/export/excel")
def export_excel():

    result = get_last_result()

    if not result:

        return {
            "success": False,
            "error": "No query results available"
        }

    df = pd.DataFrame(
        result["rows"],
        columns=result["columns"]
    )

    output_file = "exports/query_results.xlsx"

    os.makedirs(
        "exports",
        exist_ok=True
    )

    df.to_excel(
        output_file,
        index=False
    )

    return FileResponse(
        output_file,
        filename="query_results.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.delete(
    "/schema/{table_name}"
)
def delete_schema_table(
    table_name: str
):

    return delete_table(
        table_name
    )