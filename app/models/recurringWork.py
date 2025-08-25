from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, Enum, \
  TIMESTAMP, JSON,func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.enums.recurrenceType import RecurrenceType


class RecurringWork(Base):
  __tablename__ = 'recurring_work'

  id= Column(Integer, primary_key=True,index=True)
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
  title = Column(String, nullable=False)
  content = Column(String)
  category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
  myjob = Column(Boolean, nullable=False)

  #반복 설정
  recurrence_type = Column(Enum(RecurrenceType), nullable=False)
  interval_value = Column(Integer, default=1)
  started_at = Column(TIMESTAMP)
  created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(),nullable=False)
  end_at = Column(TIMESTAMP(timezone=True), nullable=False)

  #추가설정
  recurrence_config= Column(JSON,nullable =True)

  next_execution_date = Column(TIMESTAMP, nullable=False)

  #활성화
  is_active = Column(Boolean, default=True)

  updated_at = Column(TIMESTAMP)
  deleted_at = Column(TIMESTAMP, nullable=True)

  user = relationship("User", back_populates="recurring_works")
  generated_works = relationship("Work", back_populates="recurring_work")