from dataclasses import dataclass
from typing import List, Any, Optional

from .user import User

@dataclass
class Location:
    country_id: str
    region_id: str
    region_name: str
    department_id: str
    department_name: str
    city_label: str
    city: str
    zipcode: str
    lat: float
    lng: float
    source: str
    provider: str
    is_shape: bool

@dataclass
class Attribute:
    key: str
    key_label: Optional[str]
    value: str
    value_label: str
    values: List[str]
    values_label: Optional[List[str]]
    value_label_reader: Optional[str]
    generic: bool

@dataclass
class Ad:
    id: int
    first_publication_date: str
    expiration_date: str
    index_date: str
    status: str
    category_id: str
    category_name: str
    subject: str
    body: str
    brand: str
    ad_type: str
    url: str
    price: float
    images: List[str]
    attributes: List[Attribute]
    location: Location
    has_phone: bool
    favorites: int # Unvailaible on Ad from Search 

    _client: Any
    _user_id: str
    _user: User

    @staticmethod
    def _build(raw: dict, client: Any) -> "Ad":
        attributes: List[Attribute] = []
        for raw_attribute in raw.get("attributes", []):
            attributes.append(
                Attribute(
                    key=raw_attribute.get("key"),
                    key_label=raw_attribute.get("key_label"),
                    value=raw_attribute.get("value"),
                    value_label=raw_attribute.get("value_label"),
                    values=raw_attribute.get("values"),
                    values_label=raw_attribute.get("values_label"),
                    value_label_reader=raw_attribute.get("value_label_reader"),
                    generic=raw_attribute.get("generic")
                )
            )
        
        raw_location: dict = raw.get("location", {})
        location = Location(
            country_id=raw_location.get("country_id"),
            region_id=raw_location.get("region_id"),
            region_name=raw_location.get("region_name"),
            department_id=raw_location.get("department_id"),
            department_name=raw_location.get("department_name"),
            city_label=raw_location.get("city_label"),
            city=raw_location.get("city"),
            zipcode=raw_location.get("zipcode"),
            lat=raw_location.get("lat"),
            lng=raw_location.get("lng"),
            source=raw_location.get("source"),
            provider=raw_location.get("provider"),
            is_shape=raw_location.get("is_shape")
        )
        
        raw_owner: dict = raw.get("owner", {})
        return Ad(
            id=raw.get("list_id"),
            first_publication_date=raw.get("first_publication_date"),
            expiration_date=raw.get("expiration_date"),
            index_date=raw.get("index_date"),
            status=raw.get("status"),
            category_id=raw.get("category_id"),
            category_name=raw.get("category_name"),
            subject=raw.get("subject"),
            body=raw.get("body"),
            brand=raw.get("brand"),
            ad_type=raw.get("ad_type"),
            url=raw.get("url"),
            price=raw.get("price_cents") / 100 if raw.get("price_cents") else None,
            images=raw.get("images", {}).get("urls_large"),
            attributes=attributes,
            location=location,
            has_phone=raw.get("has_phone"),
            favorites=raw.get("counters", {}).get("favorites"),
            _client=client,
            _user_id=raw_owner.get("user_id"),
            _user=None
        )

    @property
    def title(self) -> str:
        return self.subject
    
    @property
    def user(self) -> User:
        if self._user is None:
            self._user = self._client.get_user(user_id=self._user_id)
        return self._user