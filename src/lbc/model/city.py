from dataclasses import dataclass


@dataclass
class City:
    lat: float
    lng: float
    radius: int = 10_000
    city: str | None = None
