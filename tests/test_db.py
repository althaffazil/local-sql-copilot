import duckdb

conn = duckdb.connect("data/sample.db")

result = conn.execute("""
SELECT
    c.customer_name,
    SUM(o.amount) AS total_amount
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
GROUP BY c.customer_name
ORDER BY total_amount DESC
""").fetchall()

print(result)

conn.close()