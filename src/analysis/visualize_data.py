import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path


# Project directory
BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "processed" / "cleaned_products.csv"

OUTPUT_DIR = BASE_DIR / "reports" / "figures"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def visualize_data():

    print("STARTING DATA VISUALIZATION")
    print("=" * 40)

    df = pd.read_csv(INPUT_FILE)

    sns.set_theme(style="whitegrid")

    # 1. Top 10 brands
    top_brands = df["brand"].value_counts().head(10)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_brands.values, y=top_brands.index)

    plt.title("Top 10 Brands by Product Count")
    plt.xlabel("Number of Products")
    plt.ylabel("Brand")
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / "top_brands.png")
    plt.close()

    # 2. Top 10 product categories
    top_categories = df["category"].value_counts().head(10)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_categories.values, y=top_categories.index)

    plt.title("Top 10 Product Categories")
    plt.xlabel("Number of Products")
    plt.ylabel("Category")
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / "category_distribution.png")
    plt.close()

    # 3. Price distribution
    prices = df["price"].dropna()

    plt.figure(figsize=(10, 6))
    sns.histplot(prices, bins=30, kde=True)

    plt.title("Product Price Distribution")
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / "price_distribution.png")
    plt.close()

    # 4. Price vs rating
    rating_data = df.dropna(subset=["price", "rating"])

    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=rating_data,
        x="price",
        y="rating"
    )

    plt.title("Product Price vs Rating")
    plt.xlabel("Price")
    plt.ylabel("Rating")
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / "price_vs_rating.png")
    plt.close()

    print("\nVISUALIZATION COMPLETED!")

    print("Charts saved in:", OUTPUT_DIR)


if __name__ == "__main__":
    visualize_data()