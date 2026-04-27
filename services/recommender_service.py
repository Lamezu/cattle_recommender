from app.db.connection import Neo4jConnection
from models.entities import Cow

class RecommenderService:
    def __init__(self):
        self.db = Neo4jConnection()

    def get_recommendations(self, farmer_id: str) -> list:
        recs = self.recommend_by_collaborative(farmer_id)
        if not recs:
            recs = self.recommend_by_breed(farmer_id)
        if not recs:
            recs = self.get_top_rated_cows()
        return recs

    def recommend_by_collaborative(self, farmer_id: str) -> list:
        query = """
        MATCH (f1:Farmer {farmer_id: $id})-[:BUYS]->(c:Cow)<-[:BUYS]-(f2:Farmer)
        MATCH (f2)-[:BUYS]->(rec:Cow)
        WHERE f1 <> f2 AND NOT (f1)-[:BUYS]->(rec)
        RETURN rec, count(*) as weight
        ORDER BY weight DESC
        LIMIT 5
        """
        result = self.db.execute_query(query, {"id": farmer_id})
        return self._map_result_to_cows(result)

    def recommend_by_breed(self, farmer_id: str) -> list:
        query = """
        MATCH (f:Farmer {farmer_id: $id})-[:VIEWED|BUYS]->(c:Cow)
        WITH f, c.breed as preferred_breed, count(*) as count
        ORDER BY count DESC LIMIT 1
        MATCH (rec:Cow {breed: preferred_breed})
        WHERE NOT (f)-[:BUYS]->(rec)
        RETURN rec
        LIMIT 5
        """
        result = self.db.execute_query(query, {"id": farmer_id})
        return self._map_result_to_cows(result)

    def get_top_rated_cows(self, limit: int = 5) -> list:
        query = """
        MATCH (c:Cow)<-[r:RATED]-(:Farmer)
        RETURN c as rec, avg(r.stars) AS avg_rating, count(r) AS total_ratings
        ORDER BY avg_rating DESC, total_ratings DESC
        LIMIT $limit
        """
        result = self.db.execute_query(query, {"limit": limit})
        return self._map_result_to_cows(result)

    def _map_result_to_cows(self, result) -> list:
        cows = []
        if not result:
            return cows
        for record in result:
            node = record['rec']
            cows.append(Cow(
                cow_id=node['cow_id'], 
                name=node.get('name', 'Vaca'),
                breed=node['breed'], 
                age=node['age'], 
                price=node['price']
            ))
        return cows
