import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from neo4j import GraphDatabase
from services.recommendation_service import RecommendationService

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_all_recommendations():
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")

    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        service = RecommendationService(driver)

        print("\n" + "="*50)
        print("  CATTLE RECOMMENDER SYSTEM - INTEGRATION TEST")
        print("="*50 + "\n")

        with driver.session() as session:
            result = session.run("MATCH (f:Farmer)-[:BUYS]->(c:Cow) RETURN f.farmer_id LIMIT 1")
            record = result.single()
            if not record:
                logging.warning("No test data found in the database.")
                return
            test_farmer_id = record["f.farmer_id"]

        print(f"[*] Testing for Farmer ID: {test_farmer_id}")
        print("-" * 50)

        print("\n[TAB] Recommended (Personalized + Fallback):")
        for cow in service.get_personalized_recommendations(test_farmer_id, limit=3):
            print(f"  - {cow['name']} (ID: {cow['cow_id']})")

        with driver.session() as session:
            result = session.run("MATCH (f:Farmer {farmer_id: $fid})-[:BUYS]->(c:Cow) RETURN c.cow_id LIMIT 1", fid=test_farmer_id)
            test_cow_id = result.single()["c.cow_id"]
    
        print(f"\n[TAB] Similar (Based on {test_cow_id}):")
        for cow in service.get_similar_cows(test_cow_id, limit=3):
            print(f"  - {cow['name']} (Score: {cow['similarity_score']})")

        print("\n[TAB] Most Purchased:")
        for cow in service.get_most_purchased_cows(limit=3):
            print(f"  - {cow['name']} (Buys: {cow['total_buys']})")

        print("\n[TAB] Most Viewed:")
        for cow in service.get_most_viewed_cows(limit=3):
            print(f"  - {cow['name']} (Views: {cow['total_views']})")

        print("\n[TAB] Top Rated:")
        for cow in service.get_top_rated_cows(limit=3):
            print(f"  - {cow['name']} (Rating: {cow['avg_rating']:.1f} stars)")

        driver.close()
        print("\n" + "="*50)
        print("  INTEGRATION TEST COMPLETED SUCCESSFULLY")
        print("="*50 + "\n")

    except Exception as e:
        logging.error(f"Failed to execute integration test: {e}")

if __name__ == "__main__":
    test_all_recommendations()
