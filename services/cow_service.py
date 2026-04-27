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

    def get_all_cows(self) -> list:
        query = "MATCH (c:Cow) RETURN c"
        result = self.db.execute_query(query)
        return [Cow(
            cow_id=r['c']['cow_id'], 
            name=r['c'].get('name', 'Vaca'),
            breed=r['c']['breed'], 
            age=r['c']['age'], 
            price=r['c']['price']
        ) for r in result] if result else []

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
