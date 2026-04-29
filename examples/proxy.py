import lbc


def main() -> None:
    # Setup proxy1
    proxy1 = lbc.Proxy(
        host="127.0.0.1",
        port=12345,
        username="username",
        password="password",
        scheme="http",
    )

    # Initialize client with proxy1
    client = lbc.Client(proxy=proxy1)

    # Setup proxy2
    proxy2 = lbc.Proxy(
        host="127.0.0.1",
        port=23456,
    )

    # Change client proxy to proxy2
    client.proxy = proxy2

    # Remove proxy
    client.proxy = None


if __name__ == "__main__":
    main()
