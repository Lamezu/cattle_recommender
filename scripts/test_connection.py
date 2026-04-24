import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.connection import Neo4jConnection

def test_connection():
    conn = Neo4jConnection()
    try:
        conn.connect()
        query = "MATCH (n) RETURN n LIMIT 5"
        result = conn.execute_query(query)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    test_connection()
