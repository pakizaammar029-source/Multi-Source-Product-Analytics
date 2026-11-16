import pandas as pd
from sqlalchemy.orm import sessionmaker

from src.load.database import engine, create_database, ProductDB, BASE_DIR

INPUT_FILE = BASE_DIR / "data" / "processed" / "cleaned_products.csv"


def load_data():
    print("\nDATABASE LOADING")
    print("=" * 40)

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Cleaned CSV not found: {INPUT_FILE}")

    create_database()

    df = pd.read_csv(INPUT_FILE)

    # Ensure product IDs are stored as strings.
    df["product_id"] = df["product_id"].astype(str)

    # Convert missing values to None for database insertion.
    df = df.astype(object).where(pd.notna(df), None)

    records = df.to_dict(orient="records")

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Replace existing records to prevent duplicate-key errors.
        session.query(ProductDB).delete(synchronize_session=False)

        products = [ProductDB(**record) for record in records]
        session.add_all(products)

        session.commit()

        print(f"Successfully loaded {len(products)} records.")
        print("Database refreshed successfully.")

    except Exception as error:
        session.rollback()
        print("Database loading failed:", error)
        raise

    finally:
        session.close()


if __name__ == "__main__":
    load_data()