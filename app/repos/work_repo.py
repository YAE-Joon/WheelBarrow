from sqlalchemy.orm import Session
from app.models.work import Work


class WorkRepository:
    def __init__(self, db:Session):
        self.db = db

    def create(self,work_data : dict) -> Work:
        db_work = Work(**work_data)
        self.db.add(db_work)
        self.db.commit()
        self.db.refresh(db_work)
        return db_work
    
