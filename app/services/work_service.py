from sqlalchemy.orm import Session
from app.repos.work_repo import WorkRepository
from datetime import datetime
from app.schemas.work_schema import WorkCreate
from app.models.category import Category
from typing import List, Optional


class WorkService : 
    def __init__(self, db: Session):
        self.work_repo = WorkRepository(db)

    def create_work(self, work:WorkCreate):
        return self.work_repo.create(work.model_dump())