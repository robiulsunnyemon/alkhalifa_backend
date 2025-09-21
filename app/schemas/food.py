# app/schemas/food.py

from pydantic import BaseModel
from typing import Optional

class FoodBase(BaseModel):
    name: str
    description: Optional[str] = None
    food_image_url: Optional[str] = None
    price: float
    category_id: int

class FoodCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int
    food_image_url: Optional[str] = "https://cdn.pixabay.com/photo/2022/02/08/02/56/shipping-7000647_1280.png"

class FoodUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    food_image_url: Optional[str] = None
    category_id: Optional[int] = None

class Category(BaseModel):
    name: str

class Rating(BaseModel):
    average_rating: float = 0.0   # default value set করলাম

    class Config:
        from_attributes = True

class FoodResponse(FoodBase):
    id: int
    category: Optional[Category]
    food_ratings: Optional[Rating] = None   # single rating object

    class Config:
        from_attributes = True
