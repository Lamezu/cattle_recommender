from services.farmer_service import FarmerService
from services.cow_service import CowService
from services.recommender_service import RecommenderService

class MainController:
    def __init__(self):
        self.farmer_svc = FarmerService()
        self.cow_svc = CowService()
        self.recommender_svc = RecommenderService()

    def get_catalog(self) -> list:
        return self.cow_svc.get_all_cows()

    def get_farmers(self) -> list:
        return self.farmer_svc.get_all_farmers()

    def get_recommendations(self, farmer_id: str) -> list:
        return self.recommender_svc.get_recommendations(farmer_id)

    def buy_cow(self, farmer_id: str, cow_id: str) -> bool:
        return self.farmer_svc.buy_cow(farmer_id, cow_id)

    def view_cow(self, farmer_id: str, cow_id: str) -> bool:
        return self.farmer_svc.view_cow(farmer_id, cow_id)

    def rate_cow(self, farmer_id: str, cow_id: str, rating: int) -> bool:
        return self.farmer_svc.rate_cow(farmer_id, cow_id, rating)
