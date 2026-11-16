import pandas as pd
import numpy as np
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    BASE_DIR / "data" / "processed" / "cleaned_products.csv"
)

OUTPUT_DIR = BASE_DIR / "reports" / "analysis"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def run_advanced_analysis():

    print("\nADVANCED PRODUCT ANALYTICS")
    print("=" * 60)

    # Load dataset
    df = pd.read_csv(INPUT_FILE)

    # Convert numerical columns safely
    numerical_columns = [
        "price",
        "rating",
        "discount_percentage"
    ]

    for column in numerical_columns:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    # --------------------------------------
    # 1. CATEGORY-WISE ANALYSIS
    # --------------------------------------

    print("\n1. CATEGORY-WISE ANALYSIS")
    print("-" * 60)

    category_analysis = (
        df.groupby("category")
        .agg(
            total_products=("product_id", "count"),
            average_price=("price", "mean"),
            average_rating=("rating", "mean"),
            average_discount=("discount_percentage", "mean")
        )
        .round(2)
        .sort_values("average_price", ascending=False)
    )

    print(category_analysis.head(10))

    category_analysis.to_csv(
        OUTPUT_DIR / "category_analysis.csv"
    )

    # --------------------------------------
    # 2. BRAND-WISE ANALYSIS
    # --------------------------------------

    print("\n2. TOP BRANDS BY PRODUCT COUNT")
    print("-" * 60)

    brand_analysis = (
        df.dropna(subset=["brand"])
        .groupby("brand")
        .agg(
            total_products=("product_id", "count"),
            average_price=("price", "mean"),
            average_rating=("rating", "mean")
        )
        .round(2)
        .sort_values("total_products", ascending=False)
    )

    print(brand_analysis.head(10))

    brand_analysis.to_csv(
        OUTPUT_DIR / "brand_analysis.csv"
    )

    print("\nTOP BRANDS BY AVERAGE RATING")
    print("-" * 60)

    # Require at least 2 rated products
    top_rated_brands = (
        df.dropna(subset=["brand", "rating"])
        .groupby("brand")
        .agg(
            total_ratings=("rating", "count"),
            average_rating=("rating", "mean")
        )
    )

    top_rated_brands = (
        top_rated_brands[
            top_rated_brands["total_ratings"] >= 2
        ]
        .sort_values("average_rating", ascending=False)
        .round(2)
    )

    print(top_rated_brands.head(10))

    # --------------------------------------
    # 3. DISCOUNT ANALYSIS
    # --------------------------------------

    print("\n3. DISCOUNT ANALYSIS")
    print("-" * 60)

    discount_data = df["discount_percentage"].dropna()

    if not discount_data.empty:

        print("Average Discount:", round(discount_data.mean(), 2))
        print("Maximum Discount:", round(discount_data.max(), 2))
        print("Minimum Discount:", round(discount_data.min(), 2))

        # NumPy-based discount classification
        df["discount_level"] = np.select(
            [
                df["discount_percentage"] < 10,
                df["discount_percentage"] < 20,
                df["discount_percentage"] >= 20
            ],
            [
                "Low",
                "Medium",
                "High"
            ],
            default="Unknown"
        )

        discount_distribution = (
            df["discount_level"].value_counts()
        )

        print("\nDiscount Level Distribution:")
        print(discount_distribution)

        discount_distribution.to_csv(
            OUTPUT_DIR / "discount_distribution.csv"
        )

    # --------------------------------------
    # 4. PRICE DISTRIBUTION USING NUMPY
    # --------------------------------------

    print("\n4. PRICE DISTRIBUTION")
    print("-" * 60)

    prices = df["price"].dropna().to_numpy()

    if len(prices) > 0:

        print("Average Price:", round(np.mean(prices), 2))
        print("Median Price:", round(np.median(prices), 2))
        print("Standard Deviation:", round(np.std(prices), 2))

        percentiles = np.percentile(
            prices, [25, 50, 75, 90, 95]
        )

        print("Price Percentiles:")
        print("25th:", round(percentiles[0], 2))
        print("50th:", round(percentiles[1], 2))
        print("75th:", round(percentiles[2], 2))
        print("90th:", round(percentiles[3], 2))
        print("95th:", round(percentiles[4], 2))

    # --------------------------------------
    # 5. CORRELATION ANALYSIS
    # --------------------------------------

    print("\n5. CORRELATION ANALYSIS")
    print("-" * 60)

    correlation = df[
        ["price", "rating", "discount_percentage"]
    ].corr(method="pearson")

    print(correlation.round(3))

    correlation.to_csv(
        OUTPUT_DIR / "correlation_analysis.csv"
    )

    # --------------------------------------
    # 6. SOURCE-WISE NUMERICAL DATA COVERAGE
    # --------------------------------------

    print("\n6. SOURCE-WISE DATA COVERAGE")
    print("-" * 60)

    source_coverage = df.groupby("data_source")[
        numerical_columns
    ].agg(
        ["count", "mean", "median"]
    ).round(2)

    print(source_coverage)

    source_coverage.to_csv(
        OUTPUT_DIR / "source_data_coverage.csv"
    )

    # --------------------------------------
    # 7. CATEGORY PIVOT TABLE
    # --------------------------------------

    print("\n7. CATEGORY-WISE PIVOT TABLE")
    print("-" * 60)

    pivot_table = pd.pivot_table(
        df,
        index="category",
        columns="data_source",
        values="product_id",
        aggfunc="count",
        fill_value=0
    )

    print(pivot_table.head(10))

    pivot_table.to_csv(
        OUTPUT_DIR / "category_source_pivot.csv"
    )

    # --------------------------------------
    # 8. SAVE SUMMARY
    # --------------------------------------

    print("\nADVANCED ANALYSIS COMPLETED")
    print("=" * 60)

    print("Total Products Analyzed:", len(df))

    print("Analysis files saved in:")
    print(OUTPUT_DIR)


if __name__ == "__main__":
    run_advanced_analysis()
