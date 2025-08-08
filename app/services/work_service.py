from sqlalchemy.orm import Session
from app.repos.work_repo import WorkRepository
from datetime import datetime
from app.schemas.work_schema import *
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
    
    def put_today_work(self, user_id:int, work_id : int,work:WorkPut):
        return self.work_repo.put_work(user_id,work_id,work)
        
    def end_work(self, user_id:int, work_id:int):
        today = datetime.now()
        return self.work_repo.end_work(user_id,work_id,today)

    def get_end_works(self,user_id:int,start:datetime,end:datetime) -> List[EndWorkResponse]:
        start_date = start
        end_date = end
        result = self.work_repo.get_end_works(user_id,start_date,end_date)

        response_list = []
        for work, category_path in result:
            response = EndWorkResponse(
                id=work.id,
                title = work.title,
                content = work.content,
                user_id = work.user_id,
                category_id = work.category_id,
                category_path = category_path,
                current_status = work.current_status,
                started_at = work.started_at,
                end_at = work.end_at,
                deadline = work.deadline,
                myjob = work.myjob
            )
            response_list.append(response)

        return response_list