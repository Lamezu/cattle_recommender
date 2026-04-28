from services.farmer_service import FarmerService
from services.cow_service import CowService
from services.recommender_service import RecommenderService

class MainController:
    def __init__(self):
        self.farmer_svc = FarmerService()
        self.cow_svc = CowService()
        self.recommender_svc = RecommenderService()

    def get_catalog(self, skip: int = 0, limit: int = 15, breed: str = None, search: str = None, sort: str = None) -> list:
        return self.cow_svc.get_all_cows(skip, limit, breed, search, sort)
    
    def get_total_cows(self, breed: str = None, search: str = None) -> int:
        return self.cow_svc.count_all_cows(breed, search)

    def get_farmers(self) -> list:
        return self.farmer_svc.get_all_farmers()

    def get_personalized_recommendations(self, farmer_id: str) -> list:
        return self.recommender_svc.get_personalized_recommendations(farmer_id)

    def get_similar_cows(self, cow_id: str) -> list:
        return self.recommender_svc.get_similar_cows(cow_id)

    def get_most_purchased(self, limit: int = 5) -> list:
        return self.recommender_svc.get_most_purchased_cows(limit)

    def get_most_viewed(self, limit: int = 5) -> list:
        return self.recommender_svc.get_most_viewed_cows(limit)

    def get_top_rated(self, breed: str = None, search: str = None, sort: str = None) -> list:
        return self.recommender_svc.get_top_rated_cows(15, breed, search, sort)

    def get_most_purchased(self, breed: str = None, search: str = None, sort: str = None) -> list:
        return self.recommender_svc.get_most_purchased_cows(15, breed, search, sort)

    def get_personalized_recommendations(self, farmer_id: str, breed: str = None, search: str = None, sort: str = None) -> list:
        return self.recommender_svc.get_personalized_recommendations(farmer_id, breed, search, sort)

    def buy_cow(self, farmer_id: str, cow_id: str) -> bool:
        return self.farmer_svc.buy_cow(farmer_id, cow_id)

    def view_cow(self, farmer_id: str, cow_id: str) -> bool:
        return self.farmer_svc.view_cow(farmer_id, cow_id)

    def rate_cow(self, farmer_id: str, cow_id: str, rating: int) -> bool:
        return self.farmer_svc.rate_cow(farmer_id, cow_id, rating)

    def register_farmer(self, farmer_id: str, name: str, security_answer: str) -> bool:
        from models.entities import Farmer
        self.farmer_svc.create_farmer(Farmer(
            farmer_id=farmer_id, 
            name=name, 
            security_answer=security_answer
        ))
        return True

    def get_purchases(self, farmer_id: str, breed: str = None, search: str = None, sort: str = None) -> list:
        return self.farmer_svc.get_purchases(farmer_id, breed, search, sort)

    def delete_purchase(self, farmer_id: str, cow_id: str) -> bool:
        return self.farmer_svc.delete_purchase(farmer_id, cow_id)
