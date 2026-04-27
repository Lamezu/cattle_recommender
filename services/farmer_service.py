from app.db.connection import Neo4jConnection
from models.entities import Farmer

class FarmerService:
    def __init__(self):
        self.db = Neo4jConnection()

    def create_farmer(self, farmer: Farmer):
        query = """
        MERGE (f:Farmer {farmer_id: $id})
        SET f.name = $name, f.location = $location
        RETURN f
        """
        params = {"id": farmer.farmer_id, "name": farmer.name, "location": farmer.location}
        self.db.execute_query(query, params)

    def get_all_farmers(self) -> list:
        query = "MATCH (f:Farmer) RETURN f"
        result = self.db.execute_query(query)
        return [Farmer(farmer_id=r['f']['farmer_id'], name=r['f']['name'], location=r['f'].get('location')) for r in result] if result else []

    def buy_cow(self, farmer_id: str, cow_id: str) -> bool:
        query = """
        MATCH (f:Farmer {farmer_id: $f_id}), (c:Cow {cow_id: $c_id})
        MERGE (f)-[r:BUYS]->(c)
        SET r.timestamp = timestamp()
        RETURN r
        """
        result = self.db.execute_query(query, {"f_id": farmer_id, "c_id": cow_id})
        return len(result) > 0

    def view_cow(self, farmer_id: str, cow_id: str) -> bool:
        query = """
        MATCH (f:Farmer {farmer_id: $f_id}), (c:Cow {cow_id: $c_id})
        MERGE (f)-[r:VIEWED]->(c)
        SET r.timestamp = timestamp()
        RETURN r
        """
        result = self.db.execute_query(query, {"f_id": farmer_id, "c_id": cow_id})
        return len(result) > 0

    def rate_cow(self, farmer_id: str, cow_id: str, rating: int) -> bool:
        query = """
        MATCH (f:Farmer {farmer_id: $f_id}), (c:Cow {cow_id: $c_id})
        MERGE (f)-[r:RATED]->(c)
        SET r.stars = $rating, r.timestamp = timestamp()
        RETURN r
        """
        params = {"f_id": farmer_id, "c_id": cow_id, "rating": rating}
        result = self.db.execute_query(query, params)
        return len(result) > 0
