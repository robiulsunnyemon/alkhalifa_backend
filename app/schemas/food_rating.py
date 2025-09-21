from pydantic import BaseModel,ConfigDict



class FoodRatingCreate(BaseModel):
    food_id: int
    stars: int


class FoodRatingResponse(BaseModel):
    food_id: int
    average_rating: float

    model_config = ConfigDict(from_attributes=True)