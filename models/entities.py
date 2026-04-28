from dataclasses import dataclass
from typing import Optional

@dataclass
class Farmer:
    farmer_id: str
    name: str
    security_answer: Optional[str] = None
    location: Optional[str] = None

@dataclass
class Cow:
    cow_id: str
    name: str
    breed: str
    age: int
    price: float
