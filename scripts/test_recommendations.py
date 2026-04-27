import sys
import os
import logging
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.recommender_service import RecommenderService
from app.db.connection import Neo4jConnection

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_all_recommendations():
    try:
        service = RecommenderService()
        db = Neo4jConnection()

        print("\n" + "="*50)
        print("  CATTLE RECOMMENDER SYSTEM - INTEGRATION TEST")
        print("="*50 + "\n")

        result = db.execute_query("MATCH (f:Farmer) RETURN f.farmer_id AS farmer_id LIMIT 1")
        
        if not result:
            logging.warning("No test data found in the database. Run test_recommender.py first.")
            return
            
        test_farmer_id = result[0]["farmer_id"]

        print(f"[*] Testing for Farmer ID: {test_farmer_id}")
        print("-" * 50)

        print("\n[1] Personalized Recommendations (Collaborative):")
        recs = service.recommend_by_collaborative(test_farmer_id)
        for r in recs:
            print(f"  -> {r.name} (ID: {r.cow_id}) - Breed: {r.breed}")

        print("\n[2] Recommendations by Breed Preference:")
        recs_breed = service.recommend_by_breed(test_farmer_id)
        for r in recs_breed:
            print(f"  -> {r.name} (ID: {r.cow_id}) - Breed: {r.breed}")

        print("\n[3] Top Rated Cows (General):")
        top_rated = service.get_top_rated_cows()
        for r in top_rated:
            print(f"  -> {r.name} (ID: {r.cow_id}) - Price: ${r.price}")

        print("\n" + "="*50)
        print("  TEST COMPLETED SUCCESSFULLY")
        print("="*50 + "\n")

    except Exception as e:
        logging.error(f"Test failed: {e}")

if __name__ == "__main__":
    test_all_recommendations()
