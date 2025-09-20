from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class CartBase(BaseModel):
    product_id: int
    quantity: int
    user_id: int


class CartCreate(BaseModel):
    product_id: int
    quantity: Optional[int] = 1



class CartUpdate(BaseModel):
    quantity: Optional[int] = None


class Food(BaseModel):
    id: int
    name: str
    price: float
    description: str
    food_image_url: Optional[str] = None

class CartResponse(CartBase):
    id: int
    food: Optional[Food] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True