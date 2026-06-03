from app.llm import generate_sql
from app.prompts import SCHEMA
from app.database import execute_query


question = "Show all orders above 1000"

sql = generate_sql(question, SCHEMA)

print("\nGenerated SQL:")
print(sql)

result = execute_query(sql)

print("\nResult:")
print(result)