from app.db.connection import Neo4jConnection
from models.entities import Cow

class CowService:
    def __init__(self):
        self.db = Neo4jConnection()

    def create_cow(self, cow: Cow):
        query = """
        MERGE (c:Cow {cow_id: $id})
        SET c.name = $name, c.breed = $breed, c.age = $age, c.price = $price
        WITH c
        MERGE (b:Breed {name: $breed})
        MERGE (c)-[:HAS_BREED]->(b)
        RETURN c
        """
        params = {
            "id": cow.cow_id, 
            "name": cow.name,
            "breed": cow.breed, 
            "age": cow.age, 
            "price": cow.price
        }
        self.db.execute_query(query, params)

    def get_all_cows(self, skip: int = 0, limit: int = 15, breed: str = None, search: str = None, sort: str = None) -> list:
        query_parts = ["MATCH (c:Cow)"]
        where_parts = []
        params = {"skip": skip, "limit": limit}

        if breed and breed != 'Todas':
            where_parts.append("c.breed = $breed")
            params["breed"] = breed
        
        if search:
            where_parts.append("(toLower(c.name) CONTAINS toLower($search) OR toLower(c.description) CONTAINS toLower($search))")
            params["search"] = search

        if where_parts:
            query_parts.append("WHERE " + " AND ".join(where_parts))

        query_parts.append("RETURN c")

        if sort == 'price_asc':
            query_parts.append("ORDER BY c.price ASC")
        elif sort == 'price_desc':
            query_parts.append("ORDER BY c.price DESC")
        else:
            query_parts.append("ORDER BY c.cow_id ASC")

        query_parts.append("SKIP $skip LIMIT $limit")
        
        query = " ".join(query_parts)
        result = self.db.execute_query(query, params)
        
        return [Cow(
            cow_id=r['c']['cow_id'], 
            name=r['c'].get('name', 'Vaca'),
            breed=r['c'].get('breed', 'Mestiza'), 
            age=r['c'].get('age', 0), 
            price=r['c'].get('price', 0.0)
        ) for r in result] if result else []

    def count_all_cows(self, breed: str = None, search: str = None) -> int:
        query_parts = ["MATCH (c:Cow)"]
        where_parts = []
        params = {}

        if breed and breed != 'Todas':
            where_parts.append("c.breed = $breed")
            params["breed"] = breed
        
        if search:
            where_parts.append("(toLower(c.name) CONTAINS toLower($search) OR toLower(c.description) CONTAINS toLower($search))")
            params["search"] = search

        if where_parts:
            query_parts.append("WHERE " + " AND ".join(where_parts))

        query_parts.append("RETURN count(c) as total")
        query = " ".join(query_parts)
        result = self.db.execute_query(query, params)
        return result[0]['total'] if result else 0

    def get_cow(self, cow_id: str):
        query = "MATCH (c:Cow {cow_id: $id}) RETURN c"
        result = self.db.execute_query(query, {"id": cow_id})
        if result:
            node = result[0]['c']
            return Cow(
                cow_id=node['cow_id'], 
                name=node.get('name', 'Vaca'),
                breed=node['breed'], 
                age=node['age'], 
                price=node['price']
            )
        return None
