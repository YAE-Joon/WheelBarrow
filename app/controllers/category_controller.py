from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.category_schema import CategoryCreate
from app.services.category_service import CategoryService

router = APIRouter(prefix="/category", tags=["category"])

@router.post("/")
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    user_id = 1
    category_service = CategoryService(db)
    return category_service.create_category(category,user_id)

@router.get("/level0")
def get_category(
    db: Session = Depends(get_db)
):
    user_id = 1
    category_service = CategoryService(db)
    return category_service.get_level0_category(user_id)
    