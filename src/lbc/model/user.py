from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Reply:
    in_minutes: int
    text: str
    rate_text: str
    rate: int
    reply_time_text: str

@dataclass
class Presence:
    status: str
    presence_text: str
    last_activity: str
    enabled: bool

@dataclass
class Badge:
    type: str
    name: str

@dataclass
class Feedback:
    overall_score: float
    cleanness: float
    communication: float
    conformity: float
    package: float
    product: float
    recommendation: float
    respect: float
    transaction: float
    user_attention: float
    received_count: float

    @property
    def score(self) -> float:
        return self.overall_score * 5 if self.overall_score else None

@dataclass
class Location:
    address: str
    district: str
    city: str
    label: str
    lat: float
    lng: float
    zipcode: str
    geo_source: str
    geo_provider: str
    region: str
    region_label: str
    department: str
    department_label: str
    country: str

@dataclass
class Review:
    author_name: str
    rating_value: int
    text: str
    review_time: str

@dataclass
class Rating:
    rating_value: int
    user_ratings_total: int
    source: str
    source_display: str
    retrieval_time: str
    url: str
    reviews: List[Review]

@dataclass
class Pro:
    online_store_id: int
    online_store_name: str
    activity_sector_id: int
    activity_sector: str
    category_id: int
    siren: str
    siret: str
    store_id: int
    active_since: str
    location: Location
    logo: str
    cover: str
    slogan: str
    description: str
    opening_hours: str
    website_url: str
    rating: Rating

@dataclass
class User:
    id: str
    name: str
    registered_at: str
    location: str
    feedback: Feedback
    profile_picture: str
    reply: Reply
    presence: Presence
    badges: List[Badge]
    total_ads: int
    store_id: int
    account_type: str
    description: str
    pro: Optional[Pro]

    @staticmethod
    def _build(user_data: dict, pro_data: Optional[dict]) -> "User":
        raw_feedback = user_data.get("feedback", {})
        feedback = Feedback(
            overall_score=raw_feedback.get("overall_score"),
            cleanness=raw_feedback.get("category_scores", {}).get("CLEANNESS"),
            communication=raw_feedback.get("category_scores", {}).get("COMMUNICATION"),
            conformity=raw_feedback.get("category_scores", {}).get("CONFORMITY"),
            package=raw_feedback.get("category_scores", {}).get("PACKAGE"),
            product=raw_feedback.get("category_scores", {}).get("PRODUCT"),
            recommendation=raw_feedback.get("category_scores", {}).get("RECOMMENDATION"),
            respect=raw_feedback.get("category_scores", {}).get("RESPECT"),
            transaction=raw_feedback.get("category_scores", {}).get("TRANSACTION"),
            user_attention=raw_feedback.get("category_scores", {}).get("USER_ATTENTION"),
            received_count=raw_feedback.get("received_count")
        )

        raw_reply = user_data.get("reply", {})
        reply = Reply(
            in_minutes=raw_reply.get("in_minutes"),
            text=raw_reply.get("text"),
            rate_text=raw_reply.get("rate_text"),
            rate=raw_reply.get("rate"),
            reply_time_text=raw_reply.get("reply_time_text")
        )

        raw_presence = user_data.get("presence", {})
        presence = Presence(
            status=raw_presence.get("status"),
            presence_text=raw_presence.get("presence_text"),
            last_activity=raw_presence.get("last_activity"),
            enabled=raw_presence.get("enabled")
        )

        badges = [
            Badge(type=badge.get("type"), name=badge.get("name"))
            for badge in user_data.get("badges", [])
        ]

        pro = None
        if pro_data:
            raw_pro_location = pro_data.get("location", {})
            pro_location = Location(
                address=raw_pro_location.get("address"),
                district=raw_pro_location.get("district"),
                city=raw_pro_location.get("city"),
                label=raw_pro_location.get("label"),
                lat=raw_pro_location.get("lat"),
                lng=raw_pro_location.get("lng"),
                zipcode=raw_pro_location.get("zipcode"),
                geo_source=raw_pro_location.get("geo_source"),
                geo_provider=raw_pro_location.get("geo_provider"),
                region=raw_pro_location.get("region"),
                region_label=raw_pro_location.get("region_label"),
                department=raw_pro_location.get("department"),
                department_label=raw_pro_location.get("dpt_label"),
                country=raw_pro_location.get("country")
            )

            raw_pro_rating = pro_data.get("rating", {})
            pro_rating_reviews = [
                Review(
                    author_name=review.get("author_name"),
                    rating_value=review.get("rating_value"),
                    text=review.get("text"),
                    review_time=review.get("review_time")
                )
                for review in raw_pro_rating.get("reviews", [])
            ]

            pro_rating = Rating(
                rating_value=raw_pro_rating.get("rating_value"),
                user_ratings_total=raw_pro_rating.get("user_ratings_total"),
                source=raw_pro_rating.get("source"),
                source_display=raw_pro_rating.get("source_display"),
                retrieval_time=raw_pro_rating.get("retrieval_time"),
                url=raw_pro_rating.get("url"),
                reviews=pro_rating_reviews
            )
            
            pro_owner = pro_data.get("owner", {})
            pro_brand = pro_data.get("brand", {})
            pro_information	= pro_data.get("information", {})
            pro = Pro(
                online_store_id=pro_data.get("online_store_id"),
                online_store_name=pro_data.get("online_store_name"),
                activity_sector_id=pro_owner.get("activitySectorID"),
                activity_sector=pro_owner.get("activitySector"),
                category_id=pro_owner.get("categoryId"),
                siren=pro_owner.get("siren"),
                siret=pro_owner.get("siret"),
                store_id=pro_owner.get("storeId"),
                active_since=pro_owner.get("activeSince"),
                location=pro_location,
                logo=pro_brand.get("logo", {}).get("large"),
                cover=pro_brand.get("cover", {}).get("large"),
                slogan=pro_brand.get("slogan"),
                description=pro_information.get("description"),
                opening_hours=pro_information.get("opening_hours"),
                website_url=pro_information.get("website_url"),
                rating=pro_rating
            )

        return User(
            id=user_data.get("user_id"),
            name=user_data.get("name"),
            registered_at=user_data.get("registered_at"),
            location=user_data.get("location"),
            feedback=feedback,
            profile_picture=user_data.get("profile_picture", {}).get("extra_large_url"),
            reply=reply,
            presence=presence,
            badges=badges,
            total_ads=user_data.get("total_ads"),
            store_id=user_data.get("store_id"),
            account_type=user_data.get("account_type"),
            description=user_data.get("description"),
            pro=pro
        )
    
    @property
    def is_pro(self):
        return self.account_type == "pro"