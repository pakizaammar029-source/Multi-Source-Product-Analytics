import pandas as pd
from pathlib import Path


# Project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Load cleaned product data
INPUT_FILE = BASE_DIR / "data" / "processed" / "cleaned_products.csv"


def run_analytics():

    print("STARTING PRODUCT ANALYTICS")
    print("=" * 45)

    df = pd.read_csv(INPUT_FILE)

    # 1. Basic statistics
    print("\n1. BASIC STATISTICS")
    print("-" * 45)

    print("Total products:", len(df))
    print("Unique brands:", df["brand"].nunique())
    print("Unique categories:", df["category"].nunique())

    # 2. Price analysis
    print("\n2. PRICE ANALYSIS")
    print("-" * 45)

    print("Average price:", round(df["price"].mean(), 2))
    print("Minimum price:", round(df["price"].min(), 2))
    print("Maximum price:", round(df["price"].max(), 2))

    # 3. Top 10 expensive products
    print("\n3. TOP 10 MOST EXPENSIVE PRODUCTS")
    print("-" * 45)

    expensive_products = df.nlargest(10, "price")

    print(
        expensive_products[
            ["product_name", "brand", "price"]
        ].to_string(index=False)
    )

    # 4. Top 10 brands
    print("\n4. TOP 10 BRANDS BY PRODUCT COUNT")
    print("-" * 45)

    top_brands = df["brand"].value_counts().head(10)

    print(top_brands.to_string())

    # 5. Category distribution
    print("\n5. CATEGORY DISTRIBUTION")
    print("-" * 45)

    categories = df["category"].value_counts()

    print(categories.to_string())

    # 6. Rating analysis
    print("\n6. RATING ANALYSIS")
    print("-" * 45)

    print("Average rating:", round(df["rating"].mean(), 2))
    print("Highest rating:", df["rating"].max())
    print("Lowest rating:", df["rating"].min())

    # 7. Discount analysis
    print("\n7. DISCOUNT ANALYSIS")
    print("-" * 45)

    print(
        "Average discount:",
        round(df["discount_percentage"].mean(), 2), "%"
    )

    print("\nPRODUCT ANALYTICS COMPLETED!")


if __name__ == "__main__":
    run_analytics()

