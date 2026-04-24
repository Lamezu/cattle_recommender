from app.db.connection import Neo4jConnection
from models.entities import Cow

class RecommenderService:
    def __init__(self):
        self.db = Neo4jConnection()

    def recommend_by_collaborative(self, farmer_id: str):
        query = """
        MATCH (f1:Farmer {id: $id})-[:BUYS]->(c:Cow)<-[:BUYS]-(f2:Farmer)
        MATCH (f2)-[:BUYS]->(rec:Cow)
        WHERE f1 <> f2 AND NOT (f1)-[:BUYS]->(rec)
        RETURN rec, count(*) as weight
        ORDER BY weight DESC
        LIMIT 5
        """
        result = self.db.execute_query(query, {"id": farmer_id})
        return self._map_result_to_cows(result)

    def recommend_by_breed(self, farmer_id: str):
        query = """
        MATCH (f:Farmer {id: $id})-[:VIEWED|BUYS]->(c:Cow)
        WITH f, c.breed as preferred_breed, count(*) as count
        ORDER BY count DESC LIMIT 1
        MATCH (rec:Cow {breed: preferred_breed})
        WHERE NOT (f)-[:BUYS]->(rec)
        RETURN rec
        LIMIT 5
        """
        result = self.db.execute_query(query, {"id": farmer_id})
        return self._map_result_to_cows(result)

    def _map_result_to_cows(self, result):
        cows = []
        for record in result:
            node = record['rec']
            cows.append(Cow(
                id=node['id'], 
                breed=node['breed'], 
                age=node['age'], 
                price=node['price']
            ))
        return cows
