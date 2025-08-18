from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

#Spring의 기본 DTO 클래스와 유사
class CategoryCreate(BaseModel):
    name : str
    parent_id : Optional[int]
    path : str
    level : Optional[int]
    content : str
    end_at : Optional[datetime] = None
    started_at : Optional[datetime] = None
    class Config:
        from_attributes = True


class CategoryEdit(BaseModel):
  name: Optional[str]
  parent_id: Optional[int]
  path: Optional[str]
  level: Optional[int]
  content: Optional[str]
  end_at: Optional[datetime] = None
  started_at: Optional[datetime] = None

  class Config:
    from_attributes = True

class CategoryLevel0Response(BaseModel):
    id : int
    name : str
    class Config:
        from_attributes = True
    
class CategoryLevel1Response(BaseModel):
    id : int
    parent_id : int
    name : str
    started_at : datetime
    end_at : datetime
    class Config:
        from_attributes = True

class CategoryResponse(BaseModel):
    id : int
    parent_id : Optional[int]
    name : str
    path : str
    content : str
    level : Optional[int]
    started_at : Optional[datetime]
    end_at : Optional[datetime]
    class Config:
        from_attributes = True
    
class CategoriesResponse(BaseModel):
    id : int
    name : str
    level : Optional[int]
    class Config:
        from_attributes = True

class CategoriesResponseWithParentId(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    name : str
    level : Optional[int]
    parent_id : Optional[int] = None