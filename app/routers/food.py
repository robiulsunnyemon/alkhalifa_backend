import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, Form, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.food import FoodModel
from app.schemas.food import FoodCreate, FoodUpdate, FoodResponse
from app.models.food_rating import FoodRatingModel

router = APIRouter(
    prefix="/foods",
    tags=["Foods"]
)

# Upload directory for food images
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "uploads/food")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------- Create ----------
@router.post("/", response_model=FoodResponse)
async def create_food(
        request: Request,
        name: str = Form(...),
        price: float = Form(...),
        category_id: int = Form(...),
        description: str = Form(None),
        per_person: int = Form(None),
        image: UploadFile = None,
        db: Session = Depends(get_db)
):
    image_url = None
    if image and image.filename:
        file_ext = image.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        with open(file_path, "wb") as f:
            f.write(await image.read())

        base_url = str(request.base_url)
        image_url = f"{base_url}uploads/food/{unique_filename}"

    db_food = FoodModel(
        name=name,
        description=description,
        price=price,
        per_person=per_person,
        category_id=category_id,
        food_image_url=image_url
    )
    db.add(db_food)
    db.commit()

    food_rating = db.query(FoodRatingModel).filter(FoodRatingModel.food_id == db_food.id).first()

    if not food_rating:
        food_rating = FoodRatingModel(
            food_id=db_food.id,
            total_ratings=5,
            total_rating_users=1,
            average_rating=5
        )
        db.add(food_rating)
        db.commit()

    db.refresh(db_food)
    return db_food


# ---------- Get all ----------
@router.get("/", response_model=list[FoodResponse])
async def get_all_foods(db: Session = Depends(get_db)):
    foods = db.query(FoodModel).all()
    return foods


# ---------- Get single ----------
@router.get("/{food_id}", response_model=FoodResponse)
async def get_food(food_id: int, db: Session = Depends(get_db)):
    food = db.query(FoodModel).filter(FoodModel.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return food


# ---------- Update ----------
@router.put("/{food_id}", response_model=FoodResponse)
async def update_food(
        food_id: int,
        data: FoodUpdate,
        db: Session = Depends(get_db)
):
    food = db.query(FoodModel).filter(FoodModel.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(food, key, value)

    db.commit()
    db.refresh(food)
    return food


# ---------- Delete ----------
@router.delete("/{food_id}")
async def delete_food(food_id: int, db: Session = Depends(get_db)):
    food = db.query(FoodModel).filter(FoodModel.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    db.delete(food)
    db.commit()
    return {"message": "Food deleted successfully"}