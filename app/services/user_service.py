from sqlalchemy.orm import Session
from app.repos.user_repo import UserRepository
from app.schemas.user_schema import UserCreate
from app.models.user import User
from typing import List, Optional

# Spring의 @Service와 동일한 역할
class UserService:
    def __init__(self, db:Session):
        self.user_repo = UserRepository(db)

    def create_user(self, user:UserCreate) -> User:
        #비지니스 로직 
        existed_user = self.user_repo.get_by_user_id(user.user_id)
        if existed_user:
            raise ValueError("Id가 존재합니다.") 
        return self.user_repo.create(user.dict())

    def get_user(self, user_id:str) -> Optional[User]:
        self.user_repo.get_by_user_id(user_id)
        return self.user_repo.get_by_user_id(user_id)
        