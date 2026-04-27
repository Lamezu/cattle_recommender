import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.entities import Farmer, Cow
from services.farmer_service import FarmerService
from services.cow_service import CowService
from services.recommender_service import RecommenderService

def test_recommendations():
    f_svc = FarmerService()
    c_svc = CowService()
    r_svc = RecommenderService()

    print("--- Iniciando Prueba de Recomendacion ---")

    c_svc.create_cow(Cow("C1", "Vaca 1", "Angus", 2, 1000.0))
    c_svc.create_cow(Cow("C2", "Vaca 2", "Angus", 3, 1200.0))
    c_svc.create_cow(Cow("C3", "Vaca 3", "Holstein", 2, 900.0))
    c_svc.create_cow(Cow("C4", "Vaca 4", "Jersey", 4, 1100.0))

    f_svc.create_farmer(Farmer("F1", "Pepe", "Madrid"))
    f_svc.create_farmer(Farmer("F2", "Maria", "Galicia"))

    f_svc.buy_cow("F2", "C1")
    f_svc.buy_cow("F2", "C2")
    f_svc.buy_cow("F1", "C1")

    print("Recomendaciones para F1 (Colaborativo):")
    recs = r_svc.recommend_by_collaborative("F1")
    for r in recs:
        print(f"- Sugerencia: {r.name} ({r.breed})")

    print("\nRecomendaciones para F1 (Por Raza):")
    recs_breed = r_svc.recommend_by_breed("F1")
    for r in recs_breed:
        print(f"- Sugerencia: {r.name} ({r.breed})")

    print("\n--- Prueba Finalizada ---")

if __name__ == "__main__":
    test_recommendations()
