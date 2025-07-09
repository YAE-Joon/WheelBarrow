from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.category_schema import CategoryCreate, CategoryLevel0Response, CategoryLevel1Response
from app.services.category_service import CategoryService
from typing import List
router = APIRouter(prefix="/category", tags=["category"])

@router.post("/")
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    user_id = 1
    category_service = CategoryService(db)
    return category_service.create_category(category,user_id)

@router.get("/level0", response_model=List[CategoryLevel0Response])
def get_category(
    db: Session = Depends(get_db)
):
    user_id = 1
    category_service = CategoryService(db)
    return category_service.get_level0_category(user_id)

@router.get("/level1", response_model=List[CategoryLevel1Response])
def get_category1(
    db: Session= Depends(get_db)
):
    user_id = 1
    category_service = CategoryService(db)
    return category_service.get_level1_category(user_id)