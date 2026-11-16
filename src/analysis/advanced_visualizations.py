import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    BASE_DIR / "data" / "processed" / "cleaned_products.csv"
)

OUTPUT_DIR = BASE_DIR / "reports" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_advanced_visualizations():

    print("\nADVANCED DATA VISUALIZATIONS")
    print("=" * 50)

    df = pd.read_csv(INPUT_FILE)

    sns.set_theme(style="whitegrid")

    # ----------------------------------
    # 1. CATEGORY-WISE AVERAGE PRICE
    # ----------------------------------

    dummy = df[df["data_source"] == "DummyJSON"].copy()

    category_prices = (
        dummy.dropna(subset=["category", "price"])
        .groupby("category")
        .agg(
            average_price=("price", "mean"),
            product_count=("product_id", "count")
        )
    )

    # Keep categories with at least 2 products
    category_prices = category_prices[
        category_prices["product_count"] >= 2
    ]

    top_categories = (
        category_prices
        .sort_values("average_price", ascending=False)
        .head(10)
        .sort_values("average_price")
    )

    plt.figure(figsize=(11, 7))

    sns.barplot(
        data=top_categories.reset_index(),
        x="average_price",
        y="category"
    )

    plt.title("Top Categories by Average Product Price")
    plt.xlabel("Average Price")
    plt.ylabel("Product Category")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "advanced_category_prices.png",
        dpi=300
    )
    plt.close()

    # ----------------------------------
    # 2. TOP BRANDS BY PRODUCT COUNT
    # ----------------------------------

    top_brands = (
        df.dropna(subset=["brand"])
        .groupby("brand")
        .size()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    plt.figure(figsize=(10, 6))

    top_brands.plot(kind="barh")

    plt.title("Top 10 Brands by Product Count")
    plt.xlabel("Number of Products")
    plt.ylabel("Brand")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "advanced_top_brands.png",
        dpi=300
    )
    plt.close()

    # ----------------------------------
    # 3. CORRELATION HEATMAP
    # ----------------------------------

    correlation = dummy[
        ["price", "rating", "discount_percentage"]
    ].corr()

    plt.figure(figsize=(8, 6))

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        vmin=-1,
        vmax=1
    )

    plt.title("Price, Rating and Discount Correlation")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "advanced_correlation_heatmap.png",
        dpi=300
    )
    plt.close()

    # ----------------------------------
    # 4. DATA SOURCE PRODUCT COMPARISON
    # ----------------------------------

    source_counts = (
        df["data_source"]
        .value_counts()
        .reset_index()
    )

    source_counts.columns = [
        "data_source",
        "product_count"
    ]

    plt.figure(figsize=(9, 6))

    sns.barplot(
        data=source_counts,
        x="data_source",
        y="product_count"
    )

    plt.title("Product Count by Data Source")
    plt.xlabel("Data Source")
    plt.ylabel("Number of Products")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "advanced_source_comparison.png",
        dpi=300
    )
    plt.close()

    print("\nFOUR ADVANCED CHARTS GENERATED SUCCESSFULLY!")

    print("Saved in:", OUTPUT_DIR)


if __name__ == "__main__":
    create_advanced_visualizations()
