from sqlalchemy.orm import Session
from app.models.category import Category
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
    
    