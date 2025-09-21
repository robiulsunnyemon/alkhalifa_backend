from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List


class Rating(BaseModel):
    average_rating: float = 0.0

    class Config:
        from_attributes = True


class Product(BaseModel):
    name: str
    description: Optional[str] = None
    food_image_url: Optional[str] = None
    price: float
    food_ratings: Optional[Rating] = None  # single rating object


class CategoryResponseWithFood(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category_image_url: Optional[str]
    foods: List[Optional[Product]]=[]
    create_time: datetime
    update_time: datetime