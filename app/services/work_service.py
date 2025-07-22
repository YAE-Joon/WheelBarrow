from sqlalchemy.orm import Session
from app.repos.work_repo import WorkRepository
from datetime import datetime
from app.schemas.work_schema import WorkCreate,TodayWorkResponse
from app.models.category import Category
from typing import List, Optional


class WorkService : 
    def __init__(self, db: Session):
        self.work_repo = WorkRepository(db)

    def create_work(self, work:WorkCreate):
        return self.work_repo.create(work.model_dump())
    
    def get_today_works(self,user_id:int) -> List[TodayWorkResponse]:
        today = datetime.now()
        works = self.work_repo.today_works(user_id,today)
        return [TodayWorkResponse.model_validate(work) for work in works]