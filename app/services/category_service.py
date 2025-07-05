from sqlalchemy.orm import Session
from app.repos.category_repo import CategoryRepository
from app.schemas.category_schema import CategoryCreate
from app.models.category import Category
from typing import List, Optional

# Spring의 @Service와 동일한 역할
class CategoryService:
    def __init__(self, db:Session):
        self.category_repo = CategoryRepository(db)

    def create_category(self, category :CategoryCreate) -> Category:
        #비지니스 로직 
        