from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum


class RecurrenceType(str, Enum):
  DAILY = "daily"
  WEEKLY = "weekly"
  MONTHLY = "monthly"
  YEARLY = "yearly"
  CUSTOM = "custom"


class RecurringWorkCreate(BaseModel):
  title: str
  content: Optional[str] = None
  category_id: Optional[int] = None
  myjob: bool = False
  user_id: Optional[int] = None
  recurrence_type: RecurrenceType
  interval_value: int = 1
  started_at: datetime
  deadline: Optional[datetime]
  end_at: Optional[datetime] = None
  recurrence_config: Optional[Dict[str, Any]] = None


class RecurringWorkResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  title: str
  content: Optional[str]
  category_id: Optional[int]
  myjob: bool
  id: int
  recurrence_type: RecurrenceType
  interval_value: int
  started_at: datetime
  deadline: Optional[datetime]
  end_at: Optional[datetime]
  next_execution_date: datetime
  is_active: bool

class RecurringWorkIdListResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int
  recurrence_type: RecurrenceType
  interval_value: int
  recurrence_config: Optional[Dict[str, Any]]
  next_execution_date: datetime
  is_active: bool

class RecurringWorkUpdate(BaseModel):
  title: Optional[str] = None
  content: Optional[str] = None
  category_id: Optional[int] = None
  myjob: Optional[bool] = None

  recurrence_type: Optional[RecurrenceType] = None
  interval_value: Optional[int] = None
  started_at: Optional[datetime] = None
  end_at: Optional[datetime] = None
  recurrence_config: Optional[Dict[str, Any]] = None
  is_active: Optional[bool] = None