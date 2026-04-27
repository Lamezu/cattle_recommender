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

    test_farmer = Farmer(farmer_id="F1", name="Victor", location="Madrid")
    farmer_svc.create_farmer(test_farmer)
    print(f"Farmer creado: {test_farmer.name}")

    test_cow = Cow(cow_id="C1", name="Vaca 1", breed="Angus", age=3, price=1500.0)
    cow_svc.create_cow(test_cow)
    print(f"Cow creada: {test_cow.breed}")

    print("Registrando interacciones...")
    farmer_svc.view_cow("F1", "C1")
    farmer_svc.rate_cow("F1", "C1", 5)
    farmer_svc.buy_cow("F1", "C1")

    retrieved_farmer = farmer_svc.get_all_farmers()
    retrieved_cow = cow_svc.get_cow("C1")

    if retrieved_farmer and retrieved_cow:
        print("Verificacion de datos: OK")
    else:
        print("Error en la recuperacion de datos")

    print("--- Verificacion Finalizada ---")

if __name__ == "__main__":
    run_verification()
