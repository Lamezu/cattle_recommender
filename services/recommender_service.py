from app.db.connection import Neo4jConnection
from models.entities import Cow

class RecommenderService:
    def __init__(self):
        self.db = Neo4jConnection()

    def get_personalized_recommendations(self, farmer_id: str) -> list:
        recs = self._recommend_by_collaborative(farmer_id)
        if not recs:
            recs = self.get_top_rated_cows(5)
        return recs

    def _recommend_by_collaborative(self, farmer_id: str) -> list:
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

    def get_similar_cows(self, cow_id: str) -> list:
        query = """
        MATCH (target:Cow {cow_id: $id})-[:HAS_BREED|LIVES_IN]->(shared)<-[:HAS_BREED|LIVES_IN]-(rec:Cow)
        WHERE rec.cow_id <> $id
        RETURN rec, count(shared) AS similarity_score
        ORDER BY similarity_score DESC
        LIMIT 5
        """
        result = self.db.execute_query(query, {"id": cow_id})
        return self._map_result_to_cows(result)

    def get_most_purchased_cows(self, limit: int = 5) -> list:
        query = """
        MATCH (rec:Cow)<-[r:BUYS]-(:Farmer)
        RETURN rec, count(r) AS total_buys
        ORDER BY total_buys DESC
        LIMIT $limit
        """
        result = self.db.execute_query(query, {"limit": limit})
        return self._map_result_to_cows(result)

    def get_most_viewed_cows(self, limit: int = 5) -> list:
        query = """
        MATCH (rec:Cow)<-[r:VIEWED]-(:Farmer)
        RETURN rec, count(r) AS total_views
        ORDER BY total_views DESC
        LIMIT $limit
        """
        result = self.db.execute_query(query, {"limit": limit})
        return self._map_result_to_cows(result)

    def get_top_rated_cows(self, limit: int = 5) -> list:
        query = """
        MATCH (rec:Cow)<-[r:RATED]-(:Farmer)
        RETURN rec, avg(r.stars) AS avg_rating, count(r) AS total_ratings
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
                breed=node.get('breed', 'Unknown'), 
                age=int(node.get('age', 0)), 
                price=float(node.get('price', 0))
            ))
        return cows
