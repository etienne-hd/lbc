from dataclasses import dataclass
from typing import Optional

@dataclass
class City:
    lat: float
    lng: float
    radius: int = 10_000
    city: Optional[str] = None