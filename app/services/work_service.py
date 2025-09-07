from sqlalchemy.orm import Session
from app.repos.work_repo import WorkRepository
from app.repos.category_repo import CategoryRepository
from datetime import datetime
from app.schemas.work_schema import *
from app.models.category import Category
from typing import List, Optional


class WorkService : 
    def __init__(self, db: Session):
        self.work_repo = WorkRepository(db)
        self.category_repo = CategoryRepository(db)

    def create_work(self, work:WorkCreate)->WorkResponse:
        work_res = self.work_repo.create(work.model_dump())
        return WorkResponse.model_validate(work_res)

    def get_today_works(self,user_id:int) -> List[TodayWorkResponse]:
        today = datetime.now()
        works = self.work_repo.today_works(user_id,today)
        
        worklist =[]

        for work in works:
            category_list = []
            category_id = work.category_id
            categories_linked_work = self.category_repo.find_categories_all(user_id,category_id)
            for category in categories_linked_work:
                category_in_work =CategoryResponse(category_id = category.id, category_name = category.name, level = category.level)
                category_list.append(category_in_work)
            result = TodayWorkResponse(
                id = work.id,
                title = work.title,
                content = work.content,
                categories = category_list,
                current_status = work.current_status,
                started_at = work.started_at,
                deadline = work.deadline,
                myjob = work.myjob,
                recurrence_type= work.recurring_work.recurrence_type if work.recurring_work else None,
                interval_value= work.recurring_work.interval_value if work.recurring_work else None,
            )

            worklist.append(result)

        return worklist


        
        return [TodayWorkResponse.model_validate(work) for work in works]
    
    def put_today_work(self, user_id:int, work_id : int,work_data:WorkPut) -> WorkEdit:
        result = self.work_repo.put_work(user_id,work_id,work_data)
        return WorkEdit.model_validate(result)

    def end_work(self, user_id:int, work_id:int):
        today = datetime.now()
        return self.work_repo.end_work(user_id,work_id,today)

    def get_end_works(self,user_id:int,start:datetime,end:datetime) -> List[EndWorkResponse]:
        start_date = start
        end_date = end
        result = self.work_repo.get_end_works(user_id,start_date,end_date)

        response_list = []
        for work, category_path in result:
            category_id_list = category_path.split('/')
            root_category_id = int(category_id_list[1])
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
                myjob = work.myjob,
                root_category_id = root_category_id
            )
            response_list.append(response)

        return response_list

    def delete_work(self, user_id:int, work_id:int) -> WorkResponse:
      today = datetime.now()
      work=self.work_repo.delete_by_work_id(user_id,work_id,today)
      return WorkResponse.model_validate(work)