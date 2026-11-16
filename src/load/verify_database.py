from sqlalchemy import text
from src.load.database import engine


def verify_database():

    print("VERIFYING SQLITE DATABASE")
    print("=" * 40)

    with engine.connect() as connection:

        # Total products
        result = connection.execute(
            text("SELECT COUNT(*) FROM products")
        )

        total_products = result.scalar()

        print("Total products in database:", total_products)

        # Products by data source
        result = connection.execute(
            text("""
                SELECT data_source, COUNT(*)
                FROM products
                GROUP BY data_source
            """)
        )

        print("\nProducts by data source:")

        for source, count in result:
            print(f"{source}: {count}")

        # Show first 5 products
        result = connection.execute(
            text("""
                SELECT product_name, brand, price, rating
                FROM products
                LIMIT 5
            """)
        )

        print("\nFIRST 5 PRODUCTS:")

        for product in result:
            print(product)


if __name__ == "__main__":
    verify_database()