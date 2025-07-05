from sqlalchemy import Column,Integer,String,TIMESTAMP,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base

# Spring의 @Entity와 동일한 역할
class Work(Base):
    __tablename__ = "work" # Spring의 @Table(name="users")와 유사

    # Spring의 @Id @GeneratedValue와 유사
    id = Column(Integer, primary_key=True, index = True)
    # Spring의 @Column과 유사
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False,index = True)
    title = Column(String, nullable=False)
    content = Column(String)
    category_id = Column(Integer, ForeignKey("category.id"))
    deadline = Column(TIMESTAMP)
    myjob = Column(Boolean, nullable= False,default =False)
    end_at = Column(TIMESTAMP)
    # Spring의 @CreationTimestamp와 유사
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable= False)
    deleted_at = Column(TIMESTAMP)

    user = relationship("User",back_populates = "works", viewonly=True)