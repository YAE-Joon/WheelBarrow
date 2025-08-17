from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
import datetime
from app.core.deps import *
from app.models.user import User
from app.schemas.category_schema import *
from app.services.category_service import CategoryService
from typing import List
router = APIRouter(prefix="/category", tags=["category"])

@router.post("/")
def create_category(
    category: CategoryCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = user.id
    category_service = CategoryService(db)
    return category_service.create_category(category,user_id)

@router.get("/level0", response_model=List[CategoryLevel0Response])
def get_category(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = user.id
    category_service = CategoryService(db)
    return category_service.get_level0_category(user_id)

@router.get("/level1", response_model=List[CategoryLevel1Response])
def get_category1(
    user: User = Depends(get_current_user),
    db: Session= Depends(get_db)
):
    user_id = user.id
    category_service = CategoryService(db)
    return category_service.get_level1_category(user_id)

@router.get("/level1/{parent_id}",response_model = List[CategoriesResponse])
def get_category1byparent_id(
    parent_id : int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = user.id
    category_service = CategoryService(db)
    return category_service.get_level1_by_parent_id(user_id,parent_id)

@router.get("/categories",response_model=List[CategoryResponse])
def this_year_categories(
    year: int = Query(description="조회할 연도"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = user.id
    category_service = CategoryService(db)
    return category_service.get_categories_by_year(user_id,year)

@router.get("/categories/{id}", response_model=List[CategoriesResponseWithParentId])
def get_categories_all(
    id : int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = user.id
    category_service = CategoryService(db)
    return category_service.get_categoires_all_by_id(user_id,id)