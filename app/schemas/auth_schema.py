from typing import Optional

from pydantic import BaseModel
from datetime import datetime

#Spring의 기본 DTO 클래스와 유사
class UserBase(BaseModel):
    user_id : str
    username : str

# Spring의 요청 DTO (RequestDTO)와 유사
class UserCreate(UserBase):
    password : str

# Spring의 응답 DTO (ResponseDTO)dhk dbtk
class UserResponse(UserBase):
    id : int
    created_at : datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    """토큰응답스키마"""
    access_token : str
    refresh_token : str
    token_type : str = "bearer"

class TokenData(BaseModel):
  """토큰 데이터 스키마"""
  user_id : Optional[str] = None

class UserInDB(BaseModel):
  """DB유저 스키마"""
  id: int
  user_id: str
  username: str
  hashed_password: str
  created_at: datetime
  class Config:
    from_attributes = True