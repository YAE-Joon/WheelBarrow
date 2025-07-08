from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base

# Spring의 @Entity와 동일한 역할
class User(Base):
    __tablename__ = "users"  # Spring의 @Table(name="users")와 유사

    # Spring의 @Id @GeneratedValue와 유사
    id = Column(Integer, primary_key=True, index=True)

    # Spring의 @Column과 유사
    user_id = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    password = Column(String)

    # Spring의 @CreationTimestamp와 유사
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # 관계 설정 - 문자열로 참조해서 순환 import 방지
    works = relationship("Work",back_populates="user")
    categories = relationship("Category", back_populates="user")