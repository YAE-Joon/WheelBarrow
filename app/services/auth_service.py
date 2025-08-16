from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password,create_access_token, create_refresh_token
from app.repos.user_repo import UserRepository
from app.schemas.auth_schema import UserCreate, UserResponse
from app.models.user import User
from typing import List, Optional

# Spring의 @Service와 동일한 역할
class AuthService:
    def __init__(self, db:Session):
        self.user_repo = UserRepository(db)

    def create_user(self, user_data:UserCreate) -> UserResponse:
        #비지니스 로직 
        existed_user = self.user_repo.get_by_user_id(user_data.user_id)
        if existed_user:
            raise ValueError("Id가 존재합니다.")

        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            user_id=user_data.user_id,
            username=user_data.username,
            hashed_password=hashed_password
        )

        user = self.user_repo.create(db_user)
        return UserResponse(
            id=user.id,
            created_at=user.created_at,
            user_id=user.user_id,
            username=user.username
        )
    def authenticate_user(self, user_id: str, password: str) -> Optional[User]:
      """사용자 인증"""
      user = self.user_repo.get_by_user_id(user_id)
      hashed_password = user.hashed_password
      if not user:
        return None

      if not verify_password(password,hashed_password):
        return None

      return user

    def create_tokens(self, user: User) -> dict:
      """액세스 토큰과 리프레시 토큰 생성"""
      access_token_data = {"sub": user.user_id, "user_id": user.id}
      refresh_token_data = {"sub": user.user_id, "user_id": user.id}

      access_token = create_access_token(access_token_data)
      refresh_token = create_refresh_token(refresh_token_data)

      return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
      }
    def get_user(self, user_id:str) -> Optional[User]:
        return self.user_repo.get_by_user_id(user_id)
        