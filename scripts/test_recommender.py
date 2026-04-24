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

    c_svc.create_cow(Cow("C1", "Angus", 2, 1000))
    c_svc.create_cow(Cow("C2", "Angus", 3, 1200))
    c_svc.create_cow(Cow("C3", "Holstein", 2, 900))
    c_svc.create_cow(Cow("C4", "Jersey", 4, 1100))

    f_svc.create_farmer(Farmer("F1", "Pepe"))
    f_svc.create_farmer(Farmer("F2", "Maria"))

    f_svc.register_buy("F2", "C1")
    f_svc.register_buy("F2", "C2")

    f_svc.register_buy("F1", "C1")

    print("Recomendaciones para F1 (Colaborativo):")
    recs = r_svc.recommend_by_collaborative("F1")
    for r in recs:
        print(f"- Sugerencia: Vaca {r.id} ({r.breed})")

    print("\nRecomendaciones para F1 (Por Raza):")
    recs_breed = r_svc.recommend_by_breed("F1")
    for r in recs_breed:
        print(f"- Sugerencia: Vaca {r.id} ({r.breed})")

    print("\n--- Prueba Finalizada ---")

if __name__ == "__main__":
    test_recommendations()
