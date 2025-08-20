from sqlalchemy import extract, and_ , or_, text
from app.models.category import Category
from datetime import timedelta,datetime
from typing import List, Optional

from app.repos.base_repo import BaseRepository


# Spring의 @Repository와 동일한 역할
# JpaRepository<User, Long>를 구현한 것과 유사
class CategoryRepository(BaseRepository):
    # Spring의 save() 메서드와 유사
    def create(self, db_category) -> Category:
        self.db.add(db_category)
        self.db.flush()
        category_id = db_category.id
        db_category.path = f"{db_category.path}/{str(category_id)}"
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    def find_by_id(self,id:int) -> Optional[Category]:
        return self.get_active_query(Category).filter(
            Category.id==id
        ).first()

    def find_id_by_path(self, path: str,user_id:int) -> Optional[int]:
        """경로로 카테고리 ID 조회"""
        result =  self.get_active_query(Category.id).filter(
            Category.path == path,
            Category.user_id == user_id
            ).first()
        return result[0] if result else None

    def find_category_by_level0(self, user_id:int) ->List[Category]:
        """연간사업이름 가져오기"""                                                  
        return self.get_active_query(Category).filter(
            Category.level ==0,
            Category.user_id == user_id
        ).all()

    def find_categories_like_path(self, path:str, user_id:int) -> List[Category]:

      return self.get_active_query(Category).filter(
          Category.path.like(f"{path}%"),
          Category.user_id == user_id
      ).all()

    def find_category_by_level1_and_date(self, user_id:int) -> List[Category]:
        """일정 가져오기"""
        now = datetime.now()
        current_month_start = datetime(now.year,now.month, 1)
        if now.month ==12:
            next_month_start = datetime(now.year+1,1,1)
        else:
            next_month_start = datetime(now.year,now.month+1,1)
        current_month_end = next_month_start - timedelta(days=1)

        return self.get_active_query(Category.id,Category.parent_id,Category.name,Category.started_at,Category.end_at).filter(
            Category.level ==1,
            Category.user_id== user_id,
            Category.started_at<= current_month_end,
            or_(
                Category.end_at.is_(None),
                Category.end_at >= current_month_start
            )
        ).all()

    def get_categories_by_year(self, user_id:int,year_start:datetime,year_end:datetime) -> List[Category]:
      return self.get_active_query(Category).filter(
          Category.user_id==user_id,
          or_(
              Category.started_at <= year_end,
              Category.started_at.is_(None),
          ),
          or_(
              Category.end_at >= year_start,
              Category.end_at.is_(None),
          )
      ).all()

    def edit_category(self, edit_category:dict) -> Category:
      db_category = self.get_active_query(Category).filter(
          Category.id == edit_category['id']
      ).first()

      if not db_category:
        raise ValueError("project not found")


      for key, value in edit_category.items():
        if hasattr(db_category, key):
          setattr(db_category, key, value)

      self.db.commit()
      self.db.refresh(db_category)
      return db_category


    def delete_category(self,id:int,user_id:int) -> Category:
      db_category = self.get_active_query(Category).filter(
          Category.id == id,
          Category.user_id == user_id
      ).first()
      if not db_category:
        raise ValueError("project not found")
      db_category.deleted_at = datetime.now()
      self.db.commit()
      self.db.refresh(db_category)
      return db_category

    def find_category_level1_by_parent_id(self,user_id:int,parent_id:int) -> list[Category]:
        return self.get_active_query(Category.id,Category.name,Category.level).filter(
            Category.parent_id == parent_id
        ).all()
    
    def find_categories_all(self,user_id:int,category_id:int) -> List[Category]:
        recursive_query = text("""
        WITH RECURSIVE ancestors AS (
            SELECT id, name, parent_id, level
            FROM category
            WHERE id = :category_id
            AND deleted_at IS NULL
            
            UNION ALL

            SELECT c.id, c.name, c.parent_id, c.level
            FROM category c
            JOIN ancestors a ON c.id = a.parent_id
            WHERE c.deleted_at IS NULL
        )
        SELECT * FROM ancestors;
    """)
        
        result = self.db.execute(recursive_query,{"category_id": category_id})
        return result.mappings().fetchall()