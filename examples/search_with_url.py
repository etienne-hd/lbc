"""Search for ads on Leboncoin using a full search URL."""

import lbc


def main() -> None:
    # Initialize the Leboncoin API client
    client = lbc.Client()

    # Perform a search using a prebuilt Leboncoin URL
    result = client.search(
        url="https://www.leboncoin.fr/recherche?category=10&text=maison&locations=Paris__48.86023250788424_2.339006433295173_9256_30000",
        page=1,
        limit=35,
    )

    # Print basic info about each ad
    for ad in result.ads:
        print(f"{ad.id} | {ad.url} | {ad.subject} | {ad.price}€ | Seller: {ad.user}")


if __name__ == "__main__":
    main()
