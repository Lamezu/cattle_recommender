from app.db.connection import Neo4jConnection
from models.entities import Farmer

class FarmerService:
    def __init__(self):
        self.db = Neo4jConnection()

    def create_farmer(self, farmer: Farmer):
        query = """
        MERGE (f:Farmer {id: $id})
        SET f.name = $name, f.location = $location
        RETURN f
        """
        params = {"id": farmer.id, "name": farmer.name, "location": farmer.location}
        self.db.execute_query(query, params)

    def get_farmer(self, farmer_id: str):
        query = "MATCH (f:Farmer {id: $id}) RETURN f"
        result = self.db.execute_query(query, {"id": farmer_id})
        if result:
            node = result[0]['f']
            return Farmer(id=node['id'], name=node['name'], location=node.get('location'))
        return None

    def delete_farmer(self, farmer_id: str):
        query = "MATCH (f:Farmer {id: $id}) DETACH DELETE f"
        self.db.execute_query(query, {"id": farmer_id})

    def register_view(self, farmer_id: str, cow_id: str):
        query = """
        MATCH (f:Farmer {id: $f_id}), (c:Cow {id: $c_id})
        MERGE (f)-[r:VIEWED]->(c)
        SET r.timestamp = timestamp()
        """
        self.db.execute_query(query, {"f_id": farmer_id, "c_id": cow_id})

    def register_buy(self, farmer_id: str, cow_id: str):
        query = """
        MATCH (f:Farmer {id: $f_id}), (c:Cow {id: $c_id})
        MERGE (f)-[r:BUYS]->(c)
        SET r.timestamp = timestamp()
        """
        self.db.execute_query(query, {"f_id": farmer_id, "c_id": cow_id})

    def register_rating(self, farmer_id: str, cow_id: str, rating: int):
        query = """
        MATCH (f:Farmer {id: $f_id}), (c:Cow {id: $c_id})
        MERGE (f)-[r:RATED]->(c)
        SET r.rating = $rating, r.timestamp = timestamp()
        """
        params = {"f_id": farmer_id, "c_id": cow_id, "rating": rating}
        self.db.execute_query(query, params)
