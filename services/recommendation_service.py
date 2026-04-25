class RecommendationService:
    def __init__(self, driver):
        self.driver = driver

    def get_most_purchased_cows(self, limit: int = 10):
        query = """
        MATCH (c:Cow)<-[r:BUYS]-(:Farmer)
        RETURN c.cow_id AS cow_id, c.name AS name, count(r) AS total_buys
        ORDER BY total_buys DESC
        LIMIT $limit
        """
        with self.driver.session() as session:
            result = session.run(query, limit=limit)
            return [record.data() for record in result]

    def get_most_viewed_cows(self, limit: int = 10):
        query = """
        MATCH (c:Cow)<-[r:VIEWED]-(:Farmer)
        RETURN c.cow_id AS cow_id, c.name AS name, count(r) AS total_views
        ORDER BY total_views DESC
        LIMIT $limit
        """
        with self.driver.session() as session:
            result = session.run(query, limit=limit)
            return [record.data() for record in result]

    def get_top_rated_cows(self, limit: int = 10):
        query = """
        MATCH (c:Cow)<-[r:RATED]-(:Farmer)
        RETURN c.cow_id AS cow_id, c.name AS name, avg(r.stars) AS avg_rating, count(r) AS total_ratings
        ORDER BY avg_rating DESC, total_ratings DESC
        LIMIT $limit
        """
        with self.driver.session() as session:
            result = session.run(query, limit=limit)
            return [record.data() for record in result]

    def get_similar_cows(self, cow_id: str, limit: int = 5):
        query = """
        MATCH (target:Cow {cow_id: $cow_id})-[:HAS_BREED|LIVES_IN]->(shared)<-[:HAS_BREED|LIVES_IN]-(other:Cow)
        WHERE other.cow_id <> $cow_id
        RETURN other.cow_id AS cow_id, other.name AS name, count(shared) AS similarity_score
        ORDER BY similarity_score DESC
        LIMIT $limit
        """
        with self.driver.session() as session:
            result = session.run(query, cow_id=cow_id, limit=limit)
            return [record.data() for record in result]

    def get_personalized_recommendations(self, farmer_id: str, limit: int = 10):
        query = """
        MATCH (me:Farmer {farmer_id: $farmer_id})-[:BUYS|VIEWED]->(shared_cow:Cow)<-[:BUYS|VIEWED]-(other:Farmer)
        MATCH (other)-[:BUYS|VIEWED]->(rec_cow:Cow)
        WHERE NOT (me)-[:BUYS|VIEWED]->(rec_cow)
        RETURN rec_cow.cow_id AS cow_id, rec_cow.name AS name, count(other) AS score
        ORDER BY score DESC
        LIMIT $limit
        """
        with self.driver.session() as session:
            result = session.run(query, farmer_id=farmer_id, limit=limit)
            recommendations = [record.data() for record in result]
            
            if not recommendations:
                return self.get_top_rated_cows(limit)
                
            return recommendations
