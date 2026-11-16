import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_FILE = BASE_DIR / "data" / "processed" / "cleaned_products.csv"
REPORT_DIR = BASE_DIR / "reports" / "analysis"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def run_submission_audit():

    print("\nFINAL PROJECT QUALITY AND EDA AUDIT")
    print("=" * 55)

    df = pd.read_csv(DATA_FILE)

    required = [
        "product_id", "product_name", "brand", "category",
        "price", "rating", "discount_percentage",
        "ingredients", "data_source"
    ]

    missing_columns = [c for c in required if c not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # 1. Dataset overview
    total = len(df)
    source_counts = df["data_source"].value_counts()

    print(f"Total records: {total}")
    print(f"Total columns: {len(df.columns)}")
    print("\nRecords by source:")
    print(source_counts.to_string())

    # 2. Validation audit
    issues = {
        "Missing product names": int(df["product_name"].isna().sum()),
        "Missing product IDs": int(df["product_id"].isna().sum()),
        "Missing data sources": int(df["data_source"].isna().sum()),
        "Duplicate source + product IDs": int(
            df.duplicated(["data_source", "product_id"]).sum()
        ),
        "Negative prices": int((df["price"].dropna() < 0).sum()),
        "Invalid ratings": int(
            ((df["rating"].dropna() < 0) |
             (df["rating"].dropna() > 5)).sum()
        ),
        "Invalid discounts": int(
            ((df["discount_percentage"].dropna() < 0) |
             (df["discount_percentage"].dropna() > 100)).sum()
        )
    }

    print("\nDATA VALIDATION AUDIT")
    for issue, count in issues.items():
        print(f"{issue}: {count}")

    pd.DataFrame(
        list(issues.items()),
        columns=["Check", "Issue Count"]
    ).to_csv(REPORT_DIR / "validation_audit.csv", index=False)

    # 3. Missing value analysis
    missing = pd.DataFrame({
        "Column": df.columns,
        "Missing_Count": df.isna().sum().values,
        "Missing_Percentage": (
            df.isna().mean().values * 100
        ).round(2)
    })

    missing.to_csv(REPORT_DIR / "missing_value_audit.csv", index=False)

    # 4. Source-wise numerical coverage
    coverage = df.groupby("data_source").agg(
        Total_Products=("product_id", "count"),
        Products_With_Price=("price", "count"),
        Products_With_Rating=("rating", "count"),
        Products_With_Discount=("discount_percentage", "count")
    )

    coverage.to_csv(REPORT_DIR / "source_coverage_audit.csv")

    # 5. Deeper statistical analysis: DummyJSON only
    dummy = df[df["data_source"] == "DummyJSON"].copy()

    numeric = dummy[
        ["price", "rating", "discount_percentage"]
    ]

    stats = numeric.describe().T
    stats["median"] = numeric.median()
    stats["skewness"] = numeric.skew()

    stats.to_csv(REPORT_DIR / "statistical_audit.csv")

    correlations = numeric.corr()
    correlations.to_csv(REPORT_DIR / "correlation_audit.csv")

    # 6. Automatic analytical findings
    findings = []

    if not dummy["price"].dropna().empty:
        price_mean = dummy["price"].mean()
        price_median = dummy["price"].median()

        if price_mean > price_median:
            findings.append(
                "Price distribution is right-skewed: "
                "the mean exceeds the median. "
                "The median may better represent a typical product price."
            )

    if not correlations.empty:
        pr = correlations.loc["price", "rating"]

        findings.append(
            f"Price-rating correlation is {pr:.3f}. "
            "This measures linear association, not causation."
        )

    if "price" in numeric:
        price = numeric["price"].dropna()

        if len(price) >= 4:
            q1 = price.quantile(0.25)
            q3 = price.quantile(0.75)
            iqr = q3 - q1

            outliers = (
                (price < q1 - 1.5 * iqr) |
                (price > q3 + 1.5 * iqr)
            ).sum()

            findings.append(
                f"Price IQR analysis flags {outliers} potential outliers. "
                "These should be investigated, not automatically deleted."
            )

    findings.append(
        "Open Beauty Facts does not provide the same price, rating "
        "and discount coverage as DummyJSON. Cross-source comparisons "
        "for these metrics are therefore not valid."
    )

    findings.append(
        "Missing values are not automatically data errors. "
        "Some fields are not supplied by the original data source."
    )

    # 7. Save human-readable report
    report_file = REPORT_DIR / "final_eda_findings.txt"

    with open(report_file, "w", encoding="utf-8") as file:
        file.write("MULTI-SOURCE E-COMMERCE PRODUCT ANALYTICS\n")
        file.write("FINAL EDA AND DATA QUALITY REPORT\n")
        file.write("=" * 55 + "\n\n")

        file.write(f"Total cleaned records: {total}\n\n")

        file.write("SOURCE DISTRIBUTION\n")
        file.write(source_counts.to_string() + "\n\n")

        file.write("DATA VALIDATION RESULTS\n")
        for issue, count in issues.items():
            file.write(f"{issue}: {count}\n")

        file.write("\nANALYTICAL FINDINGS\n")
        for index, finding in enumerate(findings, 1):
            file.write(f"{index}. {finding}\n")

    print("\nANALYTICAL FINDINGS")
    for finding in findings:
        print("-", finding)

    print("\nAudit reports saved in:", REPORT_DIR)
    print("\nFINAL AUDIT COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    run_submission_audit()
