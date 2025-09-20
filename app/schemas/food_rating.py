from pydantic import BaseModel



class FoodRatingCreate(BaseModel):
    food_id: int
    stars: int


class FoodRatingResponse(BaseModel):
    food_id: int
    average_rating: float

    class Config:
        from_attributes = True