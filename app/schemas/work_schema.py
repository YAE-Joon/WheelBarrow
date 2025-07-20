from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WorkCreate(BaseModel):
    title : str
    content : str
    user_id : int
    category_id : int
    deadline : datetime
    myjob : bool
    
class WorkResponse(BaseModel):
    title : str
    id : int

class TodayWorkResponse(BaseModel):
    title : str
    content : str
    user_id : int
    category_id : int
    deadline : datetime
    myjob : bool