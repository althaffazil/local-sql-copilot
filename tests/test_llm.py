from app.llm import generate_sql
from app.prompts import SCHEMA

question = "Show total order amount by customer"

sql = generate_sql(question, SCHEMA)

print(sql)