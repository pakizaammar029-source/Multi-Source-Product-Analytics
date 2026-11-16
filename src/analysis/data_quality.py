import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_FILE = BASE_DIR / "data" / "processed" / "cleaned_products.csv"


def analyze_data_quality():

    print("\nDATA QUALITY ANALYSIS")
    print("=" * 55)

    df = pd.read_csv(INPUT_FILE)

    print("\nDATASET OVERVIEW")
    print("-" * 55)
    print("Total Records:", len(df))
    print("Total Columns:", len(df.columns))

    # 1. Missing Values
    print("\n1. MISSING VALUES")
    print("-" * 55)

    missing = pd.DataFrame({
        "Missing Count": df.isnull().sum(),
        "Missing Percentage": (
            df.isnull().sum() / len(df) * 100
        ).round(2)
    })

    print(missing)

    # 2. Source-wise Missing Values
    print("\n2. SOURCE-WISE MISSING VALUES")
    print("-" * 55)

    for source, group in df.groupby("data_source"):

        missing_cells = group.isnull().sum().sum()
        total_cells = group.shape[0] * group.shape[1]

        percentage = missing_cells / total_cells * 100

        print(
            f"{source}: {missing_cells} missing cells "
            f"({percentage:.2f}%)"
        )

    # 3. Duplicate Records
    print("\n3. DUPLICATE ANALYSIS")
    print("-" * 55)

    duplicate_ids = df.duplicated(
        subset=["data_source", "product_id"]
    ).sum()

    duplicate_names = df.duplicated(
        subset=["product_name"],
        keep=False
    ).sum()

    print("Duplicate source + product IDs:", duplicate_ids)
    print("Records with repeated product names:", duplicate_names)

    # 4. Numerical Outlier Detection
    print("\n4. OUTLIER DETECTION (IQR)")
    print("-" * 55)

    numerical_columns = [
        "price",
        "rating",
        "discount_percentage"
    ]

    for column in numerical_columns:

        data = df[column].dropna()

        if data.empty:
            print(f"{column}: No available values")
            continue

        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = data[
            (data < lower) | (data > upper)
        ]

        print(f"{column}: {len(outliers)} potential outliers")
        print(f"  Lower boundary: {lower:.2f}")
        print(f"  Upper boundary: {upper:.2f}")

    # 5. Data Consistency Validation
    print("\n5. DATA CONSISTENCY VALIDATION")
    print("-" * 55)

    # Negative prices
    negative_prices = (df["price"].dropna() < 0).sum()

    # Ratings outside valid range
    invalid_ratings = (
        (df["rating"].dropna() < 0) |
        (df["rating"].dropna() > 5)
    ).sum()

    # Discounts outside valid range
    invalid_discounts = (
        (df["discount_percentage"].dropna() < 0) |
        (df["discount_percentage"].dropna() > 100)
    ).sum()

    # Empty or whitespace-only product names
    empty_names = (
        df["product_name"].fillna("").str.strip() == ""
    ).sum()

    # Missing essential identifiers
    missing_ids = df["product_id"].isnull().sum()
    missing_sources = df["data_source"].isnull().sum()

    print("Negative prices:", negative_prices)
    print("Invalid ratings:", invalid_ratings)
    print("Invalid discounts:", invalid_discounts)
    print("Empty product names:", empty_names)
    print("Missing product IDs:", missing_ids)
    print("Missing data sources:", missing_sources)

    # 6. Overall Quality Summary
    print("\n6. QUALITY SUMMARY")
    print("-" * 55)

    total_issues = (
        negative_prices
        + invalid_ratings
        + invalid_discounts
        + empty_names
        + missing_ids
        + missing_sources
    )

    print("Consistency issues detected:", total_issues)

    if total_issues == 0:
        print("All tested consistency rules passed.")
    else:
        print("Some consistency issues require investigation.")

    print("\nDATA QUALITY ANALYSIS COMPLETED")
    print("=" * 55)


if __name__ == "__main__":
    analyze_data_quality()