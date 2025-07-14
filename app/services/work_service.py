from sqlalchemy.orm import Session
from app.repos.category_repo import CategoryRepository
from datetime import datetime
from app.schemas.category_schema import CategoryCreate
from app.models.category import Category
from typing import List, Optional