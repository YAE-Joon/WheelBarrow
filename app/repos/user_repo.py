from sqlalchemy.orm import Session
from app.models.user import User
from typing import List, Optional

# Spring의 @Repository와 동일한 역할
# JpaRepository<User, Long>를 구현한 것과 유사
class UserRepository:
    def __init__(self,db:Session): # Spring의 EntityManager 주입과 유사
        self.db = db

    # Spring의 save() 메서드와 유사
    def create(self, user_data:dict) -> User:
        print(f"입력 데이터: {user_data}")
        db_user = User(**user_data)
        print(f"생성 직후 created_at: {db_user.created_at}")
        self.db.add(db_user)
        print(f"add 후 created_at: {db_user.created_at}")
        self.db.commit()
        print(f"commit 후 created_at: {db_user.created_at}")
        self.db.refresh(db_user)
        print(f"refresh 후 created_at: {db_user.created_at}")
        return db_user
    
    #Id로 User Id 가져오기
    def get_by_id(self, id_num:int) -> Optional[User]:
        return self.db.query(User).filter(User.id==id_num).first()

    #user_id로 user 가져오기
    def get_by_user_id(self, user_id:str) -> Optional[User]:
        return self.db.query(User).filter(User.user_id==user_id).first()