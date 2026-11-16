from pathlib import Path

from sqlalchemy import (
    create_engine,
    String,
    Float,
    Text,
    UniqueConstraint
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# SQLite database location
DATABASE_FILE = BASE_DIR / "data" / "processed" / "products.db"

# Database connection
DATABASE_URL = f"sqlite:///{DATABASE_FILE.as_posix()}"

engine = create_engine(DATABASE_URL, echo=False)


# Base class for database models
class Base(DeclarativeBase):
    pass


# Products table
class ProductDB(Base):

    __tablename__ = "products"

    __table_args__ = (
        UniqueConstraint(
            "data_source",
            "product_id",
            name="unique_source_product"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    product_id: Mapped[str] = mapped_column(String(100), nullable=False)
    product_name: Mapped[str] = mapped_column(String(500), nullable=False)

    brand: Mapped[str | None] = mapped_column(String(250), nullable=True)
    category: Mapped[str | None] = mapped_column(String(500), nullable=True)

    price: Mapped[float | None] = mapped_column(Float, nullable=True)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)

    discount_percentage: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    ingredients: Mapped[str | None] = mapped_column(Text, nullable=True)

    data_source: Mapped[str] = mapped_column(String(100), nullable=False)


# Create database and tables
def create_database():
    Base.metadata.create_all(engine)
    print("Database and tables created successfully!")
    print("Database location:", DATABASE_FILE)