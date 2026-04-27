import csv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.connection import Neo4jConnection

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def read_csv(filename: str) -> list[dict]:
    path = os.path.join(DATA_DIR, filename)
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def import_breeds(conn: Neo4jConnection) -> None:
    rows = read_csv("breeds.csv")
    conn.execute_query(
        "UNWIND $rows AS row MERGE (:Breed {name: row.name})",
        {"rows": rows},
    )
    print(f"Breeds imported:        {len(rows)}")


def import_environments(conn: Neo4jConnection) -> None:
    rows = read_csv("environments.csv")
    conn.execute_query(
        "UNWIND $rows AS row MERGE (:Environment {type: row.type})",
        {"rows": rows},
    )
    print(f"Environments imported:  {len(rows)}")


def import_cows(conn: Neo4jConnection) -> None:
    rows = read_csv("cows.csv")
    for row in rows:
        row["price"]  = float(row["price"])
        row["rating"] = float(row["rating"]) if row["rating"] else None
    conn.execute_query(
        """
        UNWIND $rows AS row
        MERGE (c:Cow {cow_id: row.cow_id})
        SET c.name        = row.name,
            c.price       = row.price,
            c.description = row.description,
            c.gender      = row.gender,
            c.rating      = row.rating
        """,
        {"rows": rows},
    )
    print(f"Cows imported:          {len(rows)}")


def import_farmers(conn: Neo4jConnection) -> None:
    rows = read_csv("farmers.csv")
    conn.execute_query(
        """
        UNWIND $rows AS row
        MERGE (f:Farmer {farmer_id: row.farmer_id})
        SET f.name            = row.name,
            f.security_answer = row.security_answer
        """,
        {"rows": rows},
    )
    print(f"Farmers imported:       {len(rows)}")


def import_has_breed(conn: Neo4jConnection) -> None:
    rows = read_csv("cows.csv")
    conn.execute_query(
        """
        UNWIND $rows AS row
        MATCH (c:Cow {cow_id: row.cow_id})
        MATCH (b:Breed {name: row.breed})
        MERGE (c)-[:HAS_BREED]->(b)
        """,
        {"rows": rows},
    )
    print(f"HAS_BREED created:      {len(rows)}")


def import_lives_in(conn: Neo4jConnection) -> None:
    rows = read_csv("cows.csv")
    conn.execute_query(
        """
        UNWIND $rows AS row
        MATCH (c:Cow {cow_id: row.cow_id})
        MATCH (e:Environment {type: row.environment})
        MERGE (c)-[:LIVES_IN]->(e)
        """,
        {"rows": rows},
    )
    print(f"LIVES_IN created:       {len(rows)}")


def import_buys(conn: Neo4jConnection) -> None:
    rows = read_csv("buys.csv")
    conn.execute_query(
        """
        UNWIND $rows AS row
        MATCH (f:Farmer {farmer_id: row.farmer_id})
        MATCH (c:Cow    {cow_id:    row.cow_id})
        MERGE (f)-[:BUYS]->(c)
        """,
        {"rows": rows},
    )
    print(f"BUYS created:           {len(rows)}")


def import_viewed(conn: Neo4jConnection) -> None:
    rows = read_csv("viewed.csv")
    conn.execute_query(
        """
        UNWIND $rows AS row
        MATCH (f:Farmer {farmer_id: row.farmer_id})
        MATCH (c:Cow    {cow_id:    row.cow_id})
        MERGE (f)-[:VIEWED]->(c)
        """,
        {"rows": rows},
    )
    print(f"VIEWED created:         {len(rows)}")


def import_rated(conn: Neo4jConnection) -> None:
    rows = read_csv("rated.csv")
    for row in rows:
        row["stars"] = int(row["stars"])
    conn.execute_query(
        """
        UNWIND $rows AS row
        MATCH (f:Farmer {farmer_id: row.farmer_id})
        MATCH (c:Cow    {cow_id:    row.cow_id})
        MERGE (f)-[r:RATED]->(c)
        SET r.stars = row.stars
        """,
        {"rows": rows},
    )
    print(f"RATED created:          {len(rows)}")


def validate(conn: Neo4jConnection) -> None:
    queries = [
        ("Farmer nodes",       "MATCH (n:Farmer)      RETURN count(n) AS total"),
        ("Cow nodes",          "MATCH (n:Cow)         RETURN count(n) AS total"),
        ("Breed nodes",        "MATCH (n:Breed)       RETURN count(n) AS total"),
        ("Environment nodes",  "MATCH (n:Environment) RETURN count(n) AS total"),
        ("BUYS",               "MATCH ()-[r:BUYS]->()     RETURN count(r) AS total"),
        ("VIEWED",             "MATCH ()-[r:VIEWED]->()   RETURN count(r) AS total"),
        ("RATED",              "MATCH ()-[r:RATED]->()    RETURN count(r) AS total"),
        ("HAS_BREED",          "MATCH ()-[r:HAS_BREED]->() RETURN count(r) AS total"),
        ("LIVES_IN",           "MATCH ()-[r:LIVES_IN]->()  RETURN count(r) AS total"),
    ]
    print("\n--- Validation ---")
    for label, query in queries:
        result = conn.execute_query(query)
        print(f"  {label:<22} {result[0]['total']:>5}")


if __name__ == "__main__":
    conn = Neo4jConnection()
    try:
        conn.connect()
        print("Connected to Neo4j.\n")

        import_breeds(conn)
        import_environments(conn)
        import_cows(conn)
        import_farmers(conn)
        import_has_breed(conn)
        import_lives_in(conn)
        import_buys(conn)
        import_viewed(conn)
        import_rated(conn)

        validate(conn)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        conn.close()
