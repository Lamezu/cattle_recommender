from app.db.connection import Neo4jConnection
from models.entities import Farmer, Cow

class FarmerService:
    def __init__(self):
        self.db = Neo4jConnection()

    def create_farmer(self, farmer: Farmer):
        query = """
        MERGE (f:Farmer {farmer_id: $id})
        SET f.name = $name, f.location = $location, f.security_answer = $answer
        RETURN f
        """
        params = {
            "id": farmer.farmer_id, 
            "name": farmer.name, 
            "location": farmer.location,
            "answer": farmer.security_answer
        }
        self.db.execute_query(query, params)

    def get_all_farmers(self) -> list:
        query = "MATCH (f:Farmer) RETURN f"
        result = self.db.execute_query(query)
        return [Farmer(
            farmer_id=r['f']['farmer_id'], 
            name=r['f']['name'], 
            security_answer=r['f'].get('security_answer')
        ) for r in result] if result else []

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

    def get_purchases(self, farmer_id: str, breed: str = None, search: str = None, sort: str = None) -> list:
        query_parts = ["MATCH (f:Farmer {farmer_id: $f_id})-[:BUYS]->(rec:Cow)"]
        where_parts = []
        params = {"f_id": farmer_id}

        if breed and breed != 'Todas':
            where_parts.append("rec.breed = $breed")
            params["breed"] = breed
        
        if search:
            where_parts.append("(toLower(rec.name) CONTAINS toLower($search) OR toLower(rec.description) CONTAINS toLower($search))")
            params["search"] = search

        if where_parts:
            query_parts.append("WHERE " + " AND ".join(where_parts))

        query_parts.append("RETURN rec")

        if sort == 'price_asc':
            query_parts.append("ORDER BY rec.price ASC")
        elif sort == 'price_desc':
            query_parts.append("ORDER BY rec.price DESC")
        else:
            query_parts.append("ORDER BY rec.cow_id ASC")

        query = " ".join(query_parts)
        result = self.db.execute_query(query, params)
        return [Cow(
            cow_id=r['rec']['cow_id'], 
            name=r['rec'].get('name', 'Vaca'),
            breed=r['rec'].get('breed', 'Mestiza'), 
            age=r['rec'].get('age', 0), 
            price=r['rec'].get('price', 0.0)
        ) for r in result] if result else []

    def delete_purchase(self, farmer_id: str, cow_id: str) -> bool:
        query = """
        MATCH (f:Farmer {farmer_id: $f_id})-[r:BUYS]->(c:Cow {cow_id: $c_id})
        DELETE r
        RETURN f
        """
        params = {"f_id": farmer_id, "c_id": cow_id}
        result = self.db.execute_query(query, params)
        return len(result) > 0
