import requests
import json
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Raw data directory
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def save_raw_data(data, filename):
    """Save original API response as JSON."""

    file_path = RAW_DIR / filename

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"Saved successfully: {file_path.name}")


def fetch_dummyjson():
    """Fetch products from DummyJSON API."""

    cached_file = RAW_DIR / "dummyjson_products.json"
    if cached_file.exists():
        with open(cached_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        print("\nUsing cached DummyJSON data.")
        print("Total products:", data.get("total", 0))
        return

    url = "https://dummyjson.com/products"

    params = {
        "limit": 0
    }

    print("\nConnecting to DummyJSON...")

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        save_raw_data(data, "dummyjson_products.json")

        print("DummyJSON connection successful!")
        print("Total products:", data.get("total", 0))

    except requests.RequestException as error:
        print("DummyJSON API error:", error)

    except ValueError as error:
        print("Invalid JSON response:", error)


def fetch_openbeautyfacts():
    """Fetch beauty products from Open Beauty Facts."""

    cached_file = RAW_DIR / "openbeautyfacts_products.json"
    if cached_file.exists():
        with open(cached_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        print("\nUsing cached Open Beauty Facts data.")
        print("Products found:", data.get("count", 0))
        return

    url = "https://world.openbeautyfacts.org/cgi/search.pl"

    params = {
        "search_terms": "skincare",
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 50
    }

    headers = {
        "User-Agent": "MultiSourceProductAnalytics/1.0"
    }

    print("\nConnecting to Open Beauty Facts...")

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        save_raw_data(data, "openbeautyfacts_products.json")

        print("Open Beauty Facts connection successful!")
        print("Products found:", data.get("count", 0))

    except requests.RequestException as error:
        print("Open Beauty Facts API error:", error)

    except ValueError as error:
        print("Invalid JSON response:", error)


if __name__ == "__main__":

    print("MULTI-SOURCE E-COMMERCE PRODUCT ANALYTICS")
    print("=" * 45)

    fetch_dummyjson()
    fetch_openbeautyfacts()

    print("\nAPI extraction process completed!")