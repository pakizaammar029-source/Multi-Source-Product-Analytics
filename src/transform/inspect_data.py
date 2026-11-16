import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"


def inspect_json(filename, source_name):

    file_path = RAW_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    print("\n" + "=" * 50)
    print(source_name)
    print("=" * 50)

    products = data.get("products", [])

    print("Total matching products:", data.get("total", data.get("count")))
    print("Downloaded products:", len(products))

    if not products:
        print("No products found!")
        return

    print("\nAvailable fields:")
    print(list(products[0].keys()))

    print("\nFirst product sample:")

    sample = products[0]

    for key, value in sample.items():
        if isinstance(value, (list, dict)):
            value = str(value)[:150]

        print(f"{key}: {value}")


if __name__ == "__main__":

    inspect_json(
        "dummyjson_products.json",
        "DUMMYJSON"
    )

    inspect_json(
        "openbeautyfacts_products.json",
        "OPEN BEAUTY FACTS"
    )