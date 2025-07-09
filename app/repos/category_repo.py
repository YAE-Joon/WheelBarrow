from sqlalchemy.orm import Session
from sqlalchemy import extract, and_ , or_
from app.models.category import Category
from datetime import timedelta,datetime
from typing import List, Optional

# Spring의 @Repository와 동일한 역할
# JpaRepository<User, Long>를 구현한 것과 유사
class CategoryRepository:
    def __init__(self,db:Session): # Spring의 EntityManager 주입과 유사
        self.db = db

    # Spring의 save() 메서드와 유사
    def create(self, category_data :dict) -> Category:
        db_category = Category(**category_data)    
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category
    
    def find_id_by_path(self, path: str,user_id:int) -> Optional[int]:
        """경로로 카테고리 ID 조회"""
        result =  self.db.query(Category.id).filter(
            Category.path == path,
            Category.user_id == user_id
            ).first()
        return result[0] if result else None
    
    def find_category_by_level0(self, user_id:int) -> list[Category]:
        """연간사업이름 가져오기"""
        return self.db.query(Category.id,Category.name).filter(
            Category.level ==0,
            Category.user_id == user_id
        ).all()
    
    def find_category_by_level1_and_date(self, user_id:int) -> list[Category]:
        """일정 가져오기"""
        now = datetime.now()
        current_month_start = datetime(now.year,now.month, 1)
        if now.month ==12:
            next_month_start = datetime(now.year+1,1,1)
        else:
            next_month_start = datetime(now.year,now.month+1,1)
        current_month_end = next_month_start - timedelta(days=1)

        return self.db.query(Category.id,Category.parent_id,Category.name,Category.started_at,Category.end_at).filter(
            Category.level ==1,
            Category.user_id== user_id,
            Category.started_at<= current_month_end,
            or_(
                Category.end_at.is_(None),
                Category.end_at >= current_month_start
            )
        ).all()