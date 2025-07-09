from pydantic import BaseModel
from datetime import datetime
from typing import Optional

#Spring의 기본 DTO 클래스와 유사
class CategoryCreate(BaseModel):
    path : str
    name : str
    content : str
    end_at : Optional[datetime] = None
    started_at : Optional[datetime] = None

class CategoryLevel0Response(BaseModel):
    id : int
    name : str
    class Config:
        from_attribute = True
    
class CategoryLevel1Response(BaseModel):
    id : int
    parent_id : int
    name : str
    started_at : datetime
    end_at : datetime
    class Config:
        from_attribute = True