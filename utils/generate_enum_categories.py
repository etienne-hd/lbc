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


def print_category(category_data: dict, category_name: str | None = None) -> None:
    label: str = category_data["label"]
    category_name: str = transform_str(category_name) if category_name else None
    label = transform_str(label)
    print(
        f'{f"{category_name}_" if category_name else ""}{label} = "{category_data["catId"]}"'
    )


def main() -> None:
    client = lbc.Client(impersonate="chrome_android")
    body = client._fetch(
        method="GET", url="https://api.leboncoin.fr/api/frontend/v1/data/v7/fdata"
    )

    for category in body["categories"]:
        print_category(category)
        if category.get("subcategories", None):
            for sub_category in category["subcategories"]:
                print_category(sub_category, category_name=category["label"])


if __name__ == "__main__":
    main()
