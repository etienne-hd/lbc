"""Search for ads on Leboncoin by location and filters (example: real estate in Paris)."""

import lbc


def main() -> None:
    # Initialize the Leboncoin API client
    client = lbc.Client()

    # Define the search location: Paris with a 10 km radius
    location = lbc.City(
        lat=48.85994982004764,
        lng=2.33801967847424,
        radius=10_000,  # 10 km
        city="Paris",
    )

    # Perform a search with various filters
    result = client.search(
        text="maison",  # Search for houses
        locations=[location],  # Only in Paris
        page=1,
        limit=35,  # Max results per page
        limit_alu=0,  # No auto-suggestions
        sort=lbc.Sort.NEWEST,  # Sort by newest ads
        ad_type=lbc.AdType.OFFER,  # Only offers, not searches
        category=lbc.Category.IMMOBILIER,  # Real estate category
        owner_type=lbc.OwnerType.ALL,  # All types of sellers
        search_in_title_only=True,  # Only search in titles
        square=(200, 400),  # Surface between 200 and 400 m²
        price=[300_000, 700_000],  # Price range in euros
    )

    # Display summary of each ad
    for ad in result.ads:
        print(f"{ad.id} | {ad.url} | {ad.subject} | {ad.price}€ | Seller: {ad.user}")


if __name__ == "__main__":
    main()
