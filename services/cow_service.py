from app.db.connection import Neo4jConnection
from models.entities import Cow

class CowService:
    def __init__(self):
        self.db = Neo4jConnection()

    def create_cow(self, cow: Cow):
        query = """
        MERGE (c:Cow {id: $id})
        SET c.breed = $breed, c.age = $age, c.price = $price
        RETURN c
        """
        params = {"id": cow.id, "breed": cow.breed, "age": cow.age, "price": cow.price}
        self.db.execute_query(query, params)

    def get_cow(self, cow_id: str):
        query = "MATCH (c:Cow {id: $id}) RETURN c"
        result = self.db.execute_query(query, {"id": cow_id})
        if result:
            node = result[0]['c']
            return Cow(id=node['id'], breed=node['breed'], age=node['age'], price=node['price'])
        return None

    def delete_cow(self, cow_id: str):
        query = "MATCH (c:Cow {id: $id}) DETACH DELETE c"
        self.db.execute_query(query, {"id": cow_id})
