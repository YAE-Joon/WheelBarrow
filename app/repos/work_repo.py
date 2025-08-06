from sqlalchemy.orm import Session
from app.models.work import Work
from datetime import timedelta,datetime
from typing import List


class WorkRepository:
    def __init__(self, db:Session):
        self.db = db

    def create(self,work_data : dict) -> Work:
        db_work = Work(**work_data)
        self.db.add(db_work)
        self.db.commit()
        self.db.refresh(db_work)
        return db_work
    
    def today_works(self,user_id:int,today:datetime) -> List[Work]:
        result = self.db.query(Work).filter(
                Work.user_id==user_id,
                Work.created_at < today,
                Work.end_at.is_(None)
                ).all()
        return  result

    def put_work(self,user_id:int,work_id:int,work_data : dict) -> Work:
        db_work = self.db.query(Work).filter(
            Work.user_id == user_id,
            Work.id == work_id
        ).first()
        if not db_work:
            return None

        update_data = work_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_work, key, value)

        self.db.commit()
        self.db.refresh(db_work)
        return db_work

    def end_work(self,user_id:int,work_id:int)-> Work:
        db_work = self.db.query(Work).filter(
            Work.user_id == user_id,
            Work.id == work_id
        ).first()

        if not db_work:
            return None
        db_work.current_status = 'DONE'
        self.db.commit()
        self.db.refresh(db_work)
        return db_work