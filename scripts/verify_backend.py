import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.entities import Farmer, Cow
from services.farmer_service import FarmerService
from services.cow_service import CowService

def run_verification():
    farmer_svc = FarmerService()
    cow_svc = CowService()

    print("--- Iniciando Verificacion ---")

    test_farmer = Farmer(id="F1", name="Victor", location="Madrid")
    farmer_svc.create_farmer(test_farmer)
    print(f"Farmer creado: {test_farmer.name}")

    test_cow = Cow(id="C1", breed="Angus", age=3, price=1500.0)
    cow_svc.create_cow(test_cow)
    print(f"Cow creada: {test_cow.breed}")

    print("Registrando interacciones...")
    farmer_svc.register_view("F1", "C1")
    farmer_svc.register_rating("F1", "C1", 5)
    farmer_svc.register_buy("F1", "C1")

    retrieved_farmer = farmer_svc.get_farmer("F1")
    retrieved_cow = cow_svc.get_cow("C1")

    if retrieved_farmer and retrieved_cow:
        print("Verificacion de datos: OK")
    else:
        print("Error en la recuperacion de datos")

    print("--- Verificacion Finalizada ---")

if __name__ == "__main__":
    run_verification()
