from dataclasses import dataclass
from typing import Optional

@dataclass
class Farmer:
    id: str
    name: str
    location: Optional[str] = None

@dataclass
class Cow:
    id: str
    breed: str
    age: int
    price: float
