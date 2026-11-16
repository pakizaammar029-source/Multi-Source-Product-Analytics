import json
import pandas as pd
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_json(filename):
    """Load raw JSON data from a file."""

    file_path = RAW_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def transform_dummyjson(data):
    """Convert DummyJSON products into standard format."""

    products = data.get("products", [])
    records = []

    for product in products:

        records.append({
            "product_id": str(product.get("id", "")),
            "product_name": product.get("title"),
            "brand": product.get("brand"),
            "category": product.get("category"),
            "price": product.get("price"),
            "rating": product.get("rating"),
            "discount_percentage": product.get("discountPercentage"),
            "ingredients": None,
            "data_source": "DummyJSON"
        })

    return pd.DataFrame(records)


def transform_openbeauty(data):
    """Convert Open Beauty Facts products into standard format."""

    products = data.get("products", [])
    records = []

    for product in products:

        records.append({
            "product_id": str(product.get("code") or product.get("_id", "")),
            "product_name": product.get("product_name_en") or product.get("product_name"),
            "brand": product.get("brands"),
            "category": product.get("categories"),
            "price": None,
            "rating": None,
            "discount_percentage": None,
            "ingredients": product.get("ingredients_text_en") or product.get("ingredients_text"),
            "data_source": "Open Beauty Facts"
        })

    return pd.DataFrame(records)


def clean_data(df):
    """Clean and standardize the combined dataset."""

    print("\nCleaning data...")

    # Remove records without product names
    df = df.dropna(subset=["product_name"])

    # Remove empty product names
    df = df[df["product_name"].astype(str).str.strip() != ""]

    # Remove duplicate products within each source
    df = df.drop_duplicates(
        subset=["data_source", "product_id"]
    )

    # Convert numeric columns
    numeric_columns = [
        "price",
        "rating",
        "discount_percentage"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Remove invalid negative prices
    df.loc[df["price"] < 0, "price"] = float("nan")

    # Reset row indexes
    df = df.reset_index(drop=True)

    return df


def main():

    print("STARTING DATA TRANSFORMATION")
    print("=" * 40)

    # Load raw datasets
    dummy_data = load_json("dummyjson_products.json")
    beauty_data = load_json("openbeautyfacts_products.json")

    print("Raw datasets loaded successfully.")

    # Transform each source
    dummy_df = transform_dummyjson(dummy_data)
    beauty_df = transform_openbeauty(beauty_data)

    print("DummyJSON records:", len(dummy_df))
    print("Open Beauty Facts records:", len(beauty_df))

    # Combine datasets
    combined_df = pd.concat(
        [dummy_df, beauty_df],
        ignore_index=True
    )

    print("Combined records:", len(combined_df))

    # Clean combined data
    cleaned_df = clean_data(combined_df)

    # Save processed data
    output_file = PROCESSED_DIR / "cleaned_products.csv"

    cleaned_df.to_csv(output_file, index=False)

    print("\nDATA CLEANING COMPLETED!")
    print("Final records:", len(cleaned_df))
    print("Saved file:", output_file)

    print("\nMissing values:")
    print(cleaned_df.isnull().sum())

    print("\nData preview:")
    print(cleaned_df.head())


if __name__ == "__main__":
    main()
