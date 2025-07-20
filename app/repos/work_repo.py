from sqlalchemy.orm import Session
from app.models.work import Work
from datetime import timedelta,datetime


class WorkRepository:
    def __init__(self, db:Session):
        self.db = db

    def create(self,work_data : dict) -> Work:
        db_work = Work(**work_data)
        self.db.add(db_work)
        self.db.commit()
        self.db.refresh(db_work)
        return db_work
    
    def today_works(self,user_id:int,datetime: datetime) -> Work:
        result = self.db.query(
            Work.title,
            Work.content,
            Work.category_id,
            Work.deadline,
            Work.myjob).filter(
                Work.user_id==user_id,
                Work.created_at < datetime,
                Work.end_at is NULL
                ).all()