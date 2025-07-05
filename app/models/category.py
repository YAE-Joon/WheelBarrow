from sqlalchemy import Column,Integer,String,TIMESTAMP,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base

# Spring의 @Entity와 동일한 역할
class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    level = Column(Integer)
    path = Column(String(1000), unique =True, nullable=False)
    name = Column(String)
    content = Column(String)
    parent_id = Column(Integer)
    end_at = Column(TIMESTAMP(timezone=True), nullabe = True)
    created_at = Column(TIMESTAMP, server_default=func.now(),nullable=False)

    works = relationship("Work",back_populates="category")