from sqlalchemy import Column, Integer, String, TIMESTAMP, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

# Spring의 @Entity와 동일한 역할
class Category(Base):
    __tablename__ = "category"

    # 복합 unique 제약조건 추가
    __table_args__ = (
        UniqueConstraint('user_id', 'id', name='uq_category_user_id'),
        UniqueConstraint('user_id', 'path', name='uq_category_user_path'),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    level = Column(Integer)
    path = Column(String(1000), nullable=False)  # unique 제거
    name = Column(String)
    content = Column(String)
    parent_id = Column(Integer, ForeignKey("category.id"))
    end_at = Column(TIMESTAMP(timezone=True), nullable=True)
    started_at = Column(TIMESTAMP(timezone=True),nullable = True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    # 관계 설정
    user = relationship("User", back_populates="categories")
    works = relationship("Work", back_populates="category",overlaps="works")

    # 자기 참조 관계
    children = relationship("Category", backref="parent", remote_side=[id])