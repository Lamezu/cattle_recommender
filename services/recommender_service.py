from app.db.connection import Neo4jConnection
from models.entities import Cow

class RecommenderService:
    def __init__(self):
        self.db = Neo4jConnection()

    def get_personalized_recommendations(self, farmer_id: str, breed: str = None, search: str = None, sort: str = None) -> list:
        recs = self._recommend_by_collaborative(farmer_id, breed, search, sort)
        if not recs:
            recs = self.get_top_rated_cows(15, breed, search, sort)
        return recs

    def _recommend_by_collaborative(self, farmer_id: str, breed: str = None, search: str = None, sort: str = None) -> list:
        query_base = """
        MATCH (f1:Farmer {farmer_id: $id})-[:BUYS]->(c:Cow)<-[:BUYS]-(f2:Farmer)
        MATCH (f2)-[:BUYS]->(rec:Cow)
        WHERE f1 <> f2 AND NOT (f1)-[:BUYS]->(rec)
        """
        where_parts, params = self._build_filters(breed, search)
        params["id"] = farmer_id
        
        query = query_base
        if where_parts:
            query += " AND " + " AND ".join(where_parts)
            
        query += " RETURN rec, count(*) as weight "
        query += self._apply_sort(sort)
        query += " LIMIT 15"
        
        result = self.db.execute_query(query, params)
        return self._map_result_to_cows(result)

    def get_most_purchased_cows(self, limit: int = 15, breed: str = None, search: str = None, sort: str = None) -> list:
        query_base = "MATCH (rec:Cow)<-[r:BUYS]-(:Farmer)"
        where_parts, params = self._build_filters(breed, search)
        params["limit"] = limit
        
        query = query_base
        if where_parts:
            query += " WHERE " + " AND ".join(where_parts)
            
        query += " RETURN rec, count(r) AS total_buys "
        query += self._apply_sort(sort, "total_buys")
        query += " LIMIT $limit"
        
        result = self.db.execute_query(query, params)
        return self._map_result_to_cows(result)

    def get_top_rated_cows(self, limit: int = 15, breed: str = None, search: str = None, sort: str = None) -> list:
        query_base = "MATCH (rec:Cow)<-[r:RATED]-(:Farmer)"
        where_parts, params = self._build_filters(breed, search)
        params["limit"] = limit
        
        query = query_base
        if where_parts:
            query += " WHERE " + " AND ".join(where_parts)
            
        query += " RETURN rec, avg(r.stars) AS avg_rating, count(r) AS total_ratings "
        query += self._apply_sort(sort, "avg_rating")
        query += " LIMIT $limit"
        
        result = self.db.execute_query(query, params)
        return self._map_result_to_cows(result)

    def _build_filters(self, breed: str, search: str):
        where_parts = []
        params = {}
        if breed and breed != 'Todas':
            where_parts.append("rec.breed = $breed")
            params["breed"] = breed
        if search:
            where_parts.append("(toLower(rec.name) CONTAINS toLower($search) OR toLower(rec.description) CONTAINS toLower($search))")
            params["search"] = search
        return where_parts, params

    def _apply_sort(self, sort: str, default_order: str = "weight"):
        if sort == 'price_asc':
            return " ORDER BY rec.price ASC "
        elif sort == 'price_desc':
            return " ORDER BY rec.price DESC "
        return f" ORDER BY {default_order} DESC "

    def _map_result_to_cows(self, result) -> list:
        cows = []
        if not result:
            return cows
        for record in result:
            node = record['rec']
            cows.append(Cow(
                cow_id=node['cow_id'], 
                name=node.get('name', 'Vaca'),
                breed=node.get('breed', 'Mestiza'), 
                age=int(node.get('age', 0)), 
                price=float(node.get('price', 0))
            ))
        return cows
