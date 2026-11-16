from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class Product(BaseModel):

    model_config = ConfigDict(
        str_strip_whitespace=True
    )

    product_id: str = Field(min_length=1)

    product_name: str = Field(min_length=1)

    brand: Optional[str] = None

    category: Optional[str] = None

    price: Optional[float] = Field(
        default=None,
        ge=0
    )

    rating: Optional[float] = Field(
        default=None,
        ge=0,
        le=5
    )

    discount_percentage: Optional[float] = Field(
        default=None,
        ge=0,
        le=100
    )

    ingredients: Optional[str] = None

    data_source: str = Field(min_length=1)