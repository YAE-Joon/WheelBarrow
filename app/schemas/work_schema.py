from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WorkCreate(BaseModel):
    title : str
    content : str
    category_id : int
    deadline : datetime
    myjob : bool
    