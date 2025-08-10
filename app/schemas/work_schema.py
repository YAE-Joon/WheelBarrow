from pydantic import BaseModel,ConfigDict
from datetime import datetime
from typing import Optional,List

class WorkCreate(BaseModel):
    title : str
    content : Optional[str]
    user_id : int
    category_id : int
    current_status : str
    started_at : Optional[datetime]
    deadline : Optional[datetime]
    myjob : bool

class WorkPut(BaseModel):
    title : str
    content : Optional[str]
    user_id : int
    category_id : int
    current_status : str
    started_at : Optional[datetime]
    deadline : Optional[datetime]
    myjob : bool

class WorkResponse(BaseModel):
    title : str
    id : int

class CategoryResponse(BaseModel):
    category_id : int
    category_name : str
    level : Optional[int]

class WorkEdit(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    title : str
    content : Optional[str]
    user_id : int
    category_id : Optional[int]
    current_status : str
    started_at : Optional[datetime]
    deadline : Optional[datetime]
    myjob : bool

class TodayWorkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    title : str
    content : Optional[str]
    user_id : int
    categories : Optional[List[CategoryResponse]]
    current_status : str
    started_at : Optional[datetime]
    deadline : Optional[datetime]
    myjob : bool

class EndWorkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    title : str
    content : Optional[str]
    user_id : int
    category_id : Optional[int]
    category_path : Optional[str]
    current_status : str
    started_at : Optional[datetime]
    end_at : datetime
    deadline : Optional[datetime]
    myjob : bool
    root_category_id : Optional[int]