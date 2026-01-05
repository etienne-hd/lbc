from dataclasses import dataclass
from typing import List, Any

from .ad import Ad

@dataclass
class Search:
    total: int
    total_all: int
    total_pro: int
    total_private: int
    total_active: int
    total_inactive: int
    total_shippable: int
    max_pages: int
    ads: List[Ad]

    @staticmethod
    def _build(raw: dict, client: Any) -> "Search":
        ads: List[Ad] = [
            Ad._build(raw=ad, client=client)
            for ad in raw.get("ads", [])
        ]

        return Search(
            total=raw.get("total"),
            total_all=raw.get("total_all"),
            total_pro=raw.get("total_pro"),
            total_private=raw.get("total_private"),
            total_active=raw.get("total_active"),
            total_inactive=raw.get("total_inactive"),
            total_shippable=raw.get("total_shippable"),
            max_pages=raw.get("max_pages"),
            ads=ads,
        )