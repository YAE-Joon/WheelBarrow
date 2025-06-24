from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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
    create_at : datetime

    class Config:
        from_attributes = True