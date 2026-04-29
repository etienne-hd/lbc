"""Get detailed information about a Leboncoin user using their user ID."""

import lbc


def main() -> None:
    # Initialize the Leboncoin API client
    client = lbc.Client()

    # Fetch a user by their Leboncoin user ID
    # Replace the ID with a real one for testing
    user = client.get_user("01234567-89ab-cdef-0123-456789abcdef")

    # Print raw user attributes
    print("User ID:", user.id)
    print("Name:", user.name)
    print("Pro status:", user.is_pro)
    print("Ads count:", user.total_ads)


if __name__ == "__main__":
    main()
