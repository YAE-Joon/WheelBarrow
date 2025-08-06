from pydantic import BaseModel,ConfigDict
from datetime import datetime
from typing import Optional

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

class TodayWorkResponse(BaseModel):
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