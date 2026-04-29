import lbc


def transform_str(string: str) -> str:
    return (
        string.strip()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("&", "et")
        .upper()
        .replace("É", "E")
        .replace("È", "E")
        .replace("Ê", "E")
        .replace("Ë", "E")
        .replace("À", "A")
        .replace("Á", "A")
        .replace("Ô", "O")
        .replace(",", "")
        .replace("___", "_")
        .replace("'", "")
    )


def print_region(region_data: dict) -> None:
    name: str = region_data["rName"]
    name = transform_str(name)
    print(f'{name} = ("{region_data["rId"]}", "{name}")')


def main() -> None:
    client = lbc.Client(impersonate="chrome_android")
    body = client._fetch(
        method="GET", url="https://api.leboncoin.fr/api/frontend/v1/data/v7/fdata"
    )

    for region in body["regions"]:
        print_region(region)


if __name__ == "__main__":
    main()
