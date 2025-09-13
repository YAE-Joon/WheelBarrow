
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager

from app.models import RecurringWork
from app.models.work import Work
from app.models.category import Category
from datetime import timedelta,datetime
from typing import List,Tuple,Optional
from app.repos.base_repo import BaseRepository

class WorkRepository(BaseRepository):

    def create(self,work_data : dict) -> Work:
        db_work = Work(**work_data)
        self.db.add(db_work)
        self.db.commit()
        self.db.refresh(db_work)
        return db_work

    def today_works(self, user_id: int, today: datetime) -> List[Work]:
      works = (self.get_active_query(
          Work,
      ).outerjoin(
          RecurringWork,
          and_(
          Work.recurring_work_id == RecurringWork.id,
          RecurringWork.deleted_at.is_(None)
          )
      ).options(
          contains_eager(Work.recurring_work)
      ).filter(
          Work.user_id == user_id,
          Work.created_at < today,
          Work.end_at.is_(None)
      ).all())
      return works

    def put_work(self,user_id:int,work_id:int,work_data : dict) -> Work:
        db_work = self.get_active_query(Work).filter(
            Work.user_id == user_id,
            Work.id == work_id
        ).first()
        if not db_work:
          raise ValueError("Work not found")

        update_data = work_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_work, key, value)

        self.db.commit()
        self.db.refresh(db_work)
        return db_work

    def end_work(self,user_id:int,work_id:int,today:datetime)-> Work:
        db_work = self.get_active_query(Work).filter(
            Work.user_id == user_id,
            Work.id == work_id
        ).first()

        if not db_work:
          raise ValueError("Work not found")
        db_work.current_status = 'DONE'
        db_work.end_at = today
        self.db.commit()
        self.db.refresh(db_work)
        return db_work

    def get_end_works(self,user_id:int,start:datetime,end:datetime) -> List[Tuple[Work, Optional[str]]]:
        return self.db.query(
            Work,
            Category.path.label('category_path')
        ).join(
            Category, Work.category_id== Category.id
        ).filter(
            Work.user_id == user_id,
            Work.deleted_at.is_(None),
            Work.end_at.is_not(None),
            Work.end_at.between(start,end)
        ).all()

    def delete_by_work_id(self,user_id:int,work_id:int, today:datetime) -> Work:
      db_work = self.db.query(
          Work
      ).filter(
          Work.id == work_id,
          Work.user_id == user_id
      ).first()

      if not db_work:
        raise ValueError("Work not found")

      db_work.deleted_at = today
      self.db.commit()
      self.db.refresh(db_work)
      return db_work
