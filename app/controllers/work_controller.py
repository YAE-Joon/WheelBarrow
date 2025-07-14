from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.category_schema import CategoryCreate, CategoryLevel0Response, CategoryLevel1Response
from app.services.category_service import CategoryService
from typing import List

router = APIRouter(prefix="/work", tags=["work"])

@router.post("/")
def create_work(
    work: CreateWork
)