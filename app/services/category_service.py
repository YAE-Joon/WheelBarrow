from sqlalchemy.orm import Session
from app.repos.category_repo import CategoryRepository
from app.schemas.category_schema import *
from app.models.category import Category
from typing import List, Optional

# Spring의 @Service와 동일한 역할
class CategoryService:
    def __init__(self, db:Session):
        self.category_repo = CategoryRepository(db)

    def create_category(self, category :CategoryCreate,user_id: int) -> CategoryResponse:
        category_with_user_id = category.model_dump()
        category_with_user_id["user_id"] = user_id
        category_create = Category(**category_with_user_id)
        category_create.created_at = datetime.now()
        result = self.category_repo.create(category_create)
        return CategoryResponse.model_validate(result)

    def get_id_by_path(self,path: str, user_id: int) -> Optional[int]:
        normal_path = self.normalize_path(path)
        return self.category_repo.find_id_by_path(normal_path, user_id)

    def get_level0_category(self,user_id: int) -> Optional[list]:
        return self.category_repo.find_category_by_level0(user_id)

    def get_level1_category(self,user_id:int) -> Optional[list]:
        return self.category_repo.find_category_by_level1_and_date(user_id)

    def get_categories_by_year(self,user_id:int,year:int) -> List[CategoryResponse]:
      year_start = datetime(year, 1, 1)
      year_end = datetime(year, 12, 31, 23, 59, 59)
      result = self.category_repo.get_categories_by_year(user_id, year_start,year_end)
      category_list = []
      for category in result:
        category_list.append(CategoryResponse.model_validate(category))
      return category_list

    def get_level1_by_parent_id(self,user_id:int,parent_id:int) -> list[CategoriesResponse]:
        return self.category_repo.find_category_level1_by_parent_id(user_id,parent_id)
        
    def get_categoires_all_by_id(self,user_id:int,id:int) -> List[CategoriesResponseWithParentId]:
        categories = self.category_repo.find_categories_all(user_id,id)
        return [CategoriesResponseWithParentId.model_validate(category) for category in categories]

    def edit_category(self,id:int,category:CategoryEdit,user_id:int) -> CategoryResponse:
        editing_category  =category.model_dump(exclude_unset=True)
        editing_category['id'] = id
        editing_category['user_id']= user_id
        edited_category = self.category_repo.edit_category(editing_category)
        return CategoryResponse.model_validate(edited_category)

    def delete_category(self,id:int,user_id:int) -> CategoryResponse:
        parent_category = self.category_repo.find_by_id(id)
        parent_path = parent_category.path
        child_categories = self.category_repo.find_categories_like_path(parent_path,user_id)
        if len(child_categories)>1:
            raise ValueError('하위 프로젝트가 존재합니다.')
        else:
            return self.category_repo.delete_category(id,user_id)

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