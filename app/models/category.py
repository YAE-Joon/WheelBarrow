from sqlalchemy import Column,Integer,String,TIMESTAMP,Boolean,ForeignKey
from sqlalchemy import relationship
from sqlalchemy.sql import func
from app.config.database import Base

# Spring의 @Entity와 동일한 역할
class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    level = Column(Integer)
    name = Column(String)
    content = Column(String)
    parent_id = Column(Integer)
    end_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)

    works = relationship("Work",back_populates="category")