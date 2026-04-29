"""Get detailed information about an ad on Leboncoin using its ID."""

import lbc


def main() -> None:
    # Initialize the Leboncoin API client
    client = lbc.Client()

    # Fetch an ad by its Leboncoin ID (replace with a real one for testing)
    ad = client.get_ad("0123456789")

    # Print basic information about the ad
    print("Title:", ad.subject)
    print("Price:", ad.price)
    print("Favorites:", ad.favorites)
    print("First published on:", ad.first_publication_date)

    # Print information about the user who posted the ad
    print("User info:", ad.user)


if __name__ == "__main__":
    main()
