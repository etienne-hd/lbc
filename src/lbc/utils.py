from typing import Optional, Union, List

from .model import Category, AdType, OwnerType, Sort, Region, Department, City
from .exceptions import InvalidValue

def build_search_payload_with_url(
    url: str,
    limit: int = 35,
    limit_alu: int = 3,
    page: int = 1
):
    def build_area(area_values: list[str]) -> dict:
        area = {
            "lat": float(area_values[0]),
            "lng": float(area_values[1])
        }
        if len(area_values) >= 3:
            area["default_radius"] = int(area_values[2])
        if len(area_values) >= 4:
            area["radius"] = int(area_values[3])
        return area
    
    payload = {
        "filters": {},
        "limit": limit,
        "limit_alu": limit_alu,
        "offset": limit * (page - 1),
        "disable_total": True,
        "extend": True,
        "listing_source": "direct-search" if page == 1 else "pagination"
    }   

    args: List[str] = url.split("?")[1].split("&")
    for arg in args:
        key, value = arg.split("=") # e.g: real_estate_type 3,4 / square 300-400 / category 9

        match key:
            case "text":
                payload["filters"]["keywords"] = {
                    "text": value
                }

            case "category":
                payload["filters"]["category"] = {
                    "id": value
                }

            case "locations":
                payload["filters"]["location"] = {
                    "locations": []
                }

                locations = value.split(",")
                for location in locations:
                    location_parts = location.split("__") # City ['Paris', '48.86023250788424_2.339006433295173_9256'], Department ['d_69'], Region ['r_18'] or Place ['p_give a star if you like it!', '0.1234567891234_-0.1234567891234567_5000_5500']

                    prefix_parts = location_parts[0].split("_")
                    if len(prefix_parts[0]) == 1: # Department ['d', '1'], Region ['r', '1'], or Place ['p', 'give a star if you like it!']
                        location_id = prefix_parts[1] # Department '1', Region '1' or Place 'give a star if you like it!'
                        match prefix_parts[0]:
                            case "d": # Department
                                payload["filters"]["location"]["locations"].append(
                                    {
                                        "locationType": "department",
                                        "department_id": location_id
                                    }
                                )
                            case "r": # Region
                                payload["filters"]["location"]["locations"].append(
                                    {
                                        "locationType": "region",
                                        "region_id": location_id
                                    }
                                )                            
                            case "p": # Place
                                area_values = location_parts[1].split("_") # lat, lng, default_radius, radius
                                payload["filters"]["location"]["locations"].append(
                                    {
                                        "locationType": "place",
                                        "place": location_id,
                                        "label": location_id,
                                        "area": build_area(area_values)
                                    }
                                )     
                            case _:
                                raise InvalidValue(f"Unknown location type: {prefix_parts[0]}")
                    
                    else: # City
                        area_values = location_parts[1].split("_") # lat, lng, default_radius, radius
                        payload["filters"]["location"]["locations"].append(
                            {
                                "locationType": "city",
                                #"city": location_parts[0],
                                "area": build_area(area_values)
                            }
                        )

            case "order":
                payload["sort_order"] = value

            case "sort":
                payload["sort_by"] = value

            case "owner_type":
                payload["owner_type"] = value

            case "shippable":
                if value == "1":
                    payload["filters"]["location"]["shippable"] = True

            case _: 
                if value in ["page"]: # Pass
                    continue
                
                # Range or Enum
                elif len(value.split("-")) == 2: # Range
                    range_values = value.split("-", 1)
                    if len(range_values) == 2:
                        min_val, max_val = range_values

                    try:
                        min_val = int(min_val)
                    except ValueError:
                        min_val = None

                    try:
                        max_val = int(max_val)
                    except ValueError:
                        max_val = None

                    if not payload["filters"].get("ranges"):
                        payload["filters"]["ranges"] = {}

                    if not payload["filters"].get("ranges"):
                        payload["filters"]["ranges"] = {}

                    ranges = {}
                    if min_val is not None:
                        ranges["min"] = min_val
                    if max_val is not None:
                        ranges["max"] = max_val

                    if ranges:
                        payload["filters"]["ranges"][key] = ranges

                else: # Enum
                    if not payload["filters"].get("enums"):
                        payload["filters"]["enums"] = {}

                    payload["filters"]["enums"][key] = value.split(",")

    return payload

def build_search_payload_with_args(
    text: Optional[str] = None,
    category: Category = Category.TOUTES_CATEGORIES,
    sort: Sort = Sort.RELEVANCE,
    locations: Optional[Union[List[Union[Region, Department, City]], Union[Region, Department, City]]] = None, 
    limit: int = 35, 
    limit_alu: int = 3, 
    page: int = 1, 
    ad_type: AdType = AdType.OFFER,
    owner_type: Optional[OwnerType] = None,
    shippable: Optional[bool] = False,
    search_in_title_only: bool = False,
    **kwargs
) -> dict:
    payload = {
        "filters": {
            "category": {
                "id": category.value
            },
            "enums": {
                "ad_type": [
                    ad_type.value
                ]
            },
            "keywords": {
                "text": text
            },
            "location": {}
        },
        "limit": limit,
        "limit_alu": limit_alu,
        "offset": limit * (page - 1),
        "disable_total": True,
        "extend": True,
        "listing_source": "direct-search" if page == 1 else "pagination"
    }   

    # Text
    if text:
        payload["filters"]["keywords"] = {
            "text": text
        }  

    # Owner Type
    if owner_type:
        payload["owner_type"] = owner_type.value

    # Sort
    sort_by, sort_order = sort.value
    payload["sort_by"] = sort_by
    if sort_order:
        payload["sort_order"] = sort_order
        
    # Location
    if locations and not isinstance(locations, list):
        locations = [locations]
        
    if locations:
        payload["filters"]["location"] = {
            "locations": []
        }
        for location in locations:
            match location:
                case Region():
                    payload["filters"]["location"]["locations"].append(
                        {
                            "locationType": "region",
                            "region_id": location.value[0]
                        }
                    )
                case Department():
                    payload["filters"]["location"]["locations"].append(
                        {
                            "locationType": "department",
                            "region_id": location.value[0],
                            "department_id": location.value[2]
                        }
                    )
                case City():
                    payload["filters"]["location"]["locations"].append(
                        {
                            "area": {
                                "lat": location.lat,
                                "lng": location.lng,
                                "radius": location.radius
                            },
                            "city": location.city,
                            "label": f"{location.city} (toute la ville)" if location.city else None,
                            "locationType": "city"
                        }
                    )
                case _:
                    raise InvalidValue("The provided location is invalid. It must be an instance of Region, Department, or City.")

    # Search in title only
    if text:
        if search_in_title_only:
            payload["filters"]["keywords"]["type"] = "subject"

    if shippable:
        payload["filters"]["location"]["shippable"] = True

    if kwargs:
        for key, value in kwargs.items():
            if not isinstance(value, (list, tuple)):
                raise InvalidValue(f"The value of '{key}' must be a list or a tuple.")  
            # Range
            if all(isinstance(x, int) for x in value):
                if len(value) <= 1:
                    raise InvalidValue(f"The value of '{key}' must be a list or tuple with at least two elements.")

                if not "ranges" in payload["filters"]:
                    payload["filters"]["ranges"] = {}

                payload["filters"]["ranges"][key] = {
                    "min": value[0],
                    "max": value[1]
                }   
            # Enum
            elif all(isinstance(x, str) for x in value):
                payload["filters"]["enums"][key] = value
            else:
                raise InvalidValue(f"The value of '{key}' must be a list or tuple containing only integers or only strings.")
            
    return payload