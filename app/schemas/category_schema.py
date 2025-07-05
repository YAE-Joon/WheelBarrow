from pydantic import BaseModel
from datetime import datetime
from typing import Optional

#Spring의 기본 DTO 클래스와 유사
class CategoryCreate(BaseModel):
    level : int
    path : str
    name : str
    content : str
    parent_id : Optional[int] = None
    end_at : Optional[datetime] = None
