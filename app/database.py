import duckdb
from app.config import DB_PATH

def create_database():
    conn = duckdb.connect(DB_PATH)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        customer_name VARCHAR,
        city VARCHAR
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        amount DECIMAL(10,2),
        order_date DATE
    )
    """)

    conn.execute("DELETE FROM customers")
    conn.execute("DELETE FROM orders")

    conn.execute("""
    INSERT INTO customers VALUES
    (1, 'Alice', 'Chennai'),
    (2, 'Bob', 'Bangalore'),
    (3, 'Charlie', 'Hyderabad'),
    (4, 'David', 'Mumbai')
    """)

    conn.execute("""
    INSERT INTO orders VALUES
    (101, 1, 1200, '2026-05-01'),
    (102, 1, 1500, '2026-05-10'),
    (103, 2, 2000, '2026-05-05'),
    (104, 2, 3000, '2026-05-15'),
    (105, 2, 4000, '2026-05-20'),
    (106, 3, 500, '2026-05-18'),
    (107, 4, 800, '2026-05-21')
    """)

    conn.close()

def execute_query(sql: str):
    conn = duckdb.connect(DB_PATH)

    try:
        result = conn.execute(sql).fetchall()
        columns = [col[0] for col in conn.description]

        return {
            "success": True,
            "columns": columns,
            "rows": result
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        conn.close()





if __name__ == "__main__":
    create_database()
    print("Database created successfully.")