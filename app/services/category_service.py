from sqlalchemy.orm import Session
from app.repos.category_repo import CategoryRepository
from datetime import datetime
from app.schemas.category_schema import CategoryCreate
from app.models.category import Category
from typing import List, Optional

# Spring의 @Service와 동일한 역할
class CategoryService:
    def __init__(self, db:Session):
        self.category_repo = CategoryRepository(db)

    def create_category(self, category :CategoryCreate,user_id: int) -> Category:
        normalize_path = self.normalize_path(category.path)
        category_data = category.model_dump()

        #user_id 추가
        category_data['user_id'] = user_id

        #parent_id를 조회 후 추가
        parent_id = None
        if normalize_path !="/" and '/' in normalize_path:
            parent_path = normalize_path.rsplit('/',1)[0]
            if parent_path =="":
                parent_path ="/"
            parent_id = self.get_id_by_path(parent_path, user_id)
        
        # 딕셔너리에 parent_id 추가
        category_data['parent_id'] = parent_id
        # 딕셔너리에 level 추가
        level = self.calculate_level(normalize_path)
        category_data['level'] = level
        return self.category_repo.create(category_data)

    def get_id_by_path(self,path: str, user_id: int) -> Optional[int]:
        normal_path = self.normalize_path(path)
        return self.category_repo.find_id_by_path(normal_path, user_id)

    def get_level0_category(self,user_id: int) -> Optional[list]:
        return self.category_repo.find_category_by_level0(user_id)


    def normalize_path(self, path: str) -> str:
        """경로 정규화: 다양한 입력을 일관된 형태로 변환"""
        # 앞뒤 공백 제거
        path = path.strip()

        # 빈 문자열이나 "/"면 루트 반환
        if not path or path == "/":
            return "/"
        
        # 앞뒤 슬래시 제거
        clean_path = path.strip('/')

        # 이중 슬래시 제거
        while '//' in clean_path:
            clean_path = clean_path.replace('//', '/')  # clean_path 자체를 업데이트
        
        return f"/{clean_path}"
    
    def calculate_level(self, normalize_path: str) -> int:
        #root 는 레벨이 없음.
        if normalize_path == "/":
            return 0
        #'/'수 -1 = level
        return normalize_path.count('/')-1