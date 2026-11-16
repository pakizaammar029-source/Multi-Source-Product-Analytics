import pandas as pd
from pathlib import Path
from collections import Counter
from pydantic import ValidationError
from src.validation.schemas import Product

# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Input CSV file
INPUT_FILE = BASE_DIR / "data" / "processed" / "cleaned_products.csv"


def validate_products():

    print("STARTING PYDANTIC VALIDATION")
    print("=" * 40)

    # Load cleaned dataset
    df = pd.read_csv(INPUT_FILE)

    valid_products = []
    invalid_products = []

    # Validate each product
    for index, row in df.iterrows():

        # Convert Pandas NaN values to None
        record = {
            key: (None if pd.isna(value) else value)
            for key, value in row.to_dict().items()
        }

        # Convert product ID to string
        if record["product_id"] is not None:
            record["product_id"] = str(record["product_id"])

        try:
            product = Product(**record)
            valid_products.append(product.model_dump())

        except ValidationError as error:
            invalid_products.append({
                "row": index,
                "errors": error.errors()
            })

    # Display validation statistics
    print("\nVALIDATION SUMMARY")
    print("-" * 40)

    print("Total records:", len(df))
    print("Valid records:", len(valid_products))
    print("Invalid records:", len(invalid_products))

    # Display first 5 invalid records
    print("\nFIRST 5 INVALID RECORDS")
    print("-" * 40)

    for item in invalid_products[:5]:

        print(f"\nRow: {item['row']}")

        for error in item["errors"]:
            print(
                f"Field: {error['loc'][0]} | "
                f"Error: {error['msg']}"
            )

    # Count common validation errors
    error_types = Counter()

    for item in invalid_products:
        for error in item["errors"]:
            error_types[
                (error["loc"][0], error["type"], error["msg"])
            ] += 1

    # Display most common errors
    print("\nMOST COMMON VALIDATION ERRORS")
    print("-" * 40)

    if error_types:
        for (field, error_type, message), count in error_types.most_common(10):
            print(
                f"{count} records | "
                f"Field: {field} | "
                f"Error: {message}"
            )
    else:
        print("No validation errors found.")

    print("\nVALIDATION COMPLETED!")


if __name__ == "__main__":
    validate_products()