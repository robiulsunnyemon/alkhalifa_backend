## app.models.food.py

from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.db import Base

class FoodModel(Base):
    __tablename__ = "foods"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    food_image_url = Column(String,default="https://picsum.photos/100/100?random=5")
    price = Column(Float)
    per_person = Column(Integer)
    category_id = Column(Integer, ForeignKey("food_categories.id", ondelete="CASCADE"))

    # String notation
    category = relationship("FoodCategoryModel", back_populates="foods")
    cart=relationship("CartModel", back_populates="food",cascade="all, delete-orphan")
    food_ratings = relationship("FoodRatingModel", back_populates="food", uselist=False,cascade="all, delete-orphan")
    order_items=relationship("OrderItemModel", back_populates="food",cascade="all, delete-orphan")