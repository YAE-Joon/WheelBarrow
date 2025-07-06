from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base

# Spring의 @Entity와 동일한 역할
class Work(Base):
    __tablename__ = "work"

    # 복합 외래키 제약조건
    __table_args__ = (
        ForeignKeyConstraint(
            ['user_id', 'category_id'],
            ['category.user_id', 'category.id'],
            name='fk_work_category_user'
        ),
    )

    # Spring의 @Id @GeneratedValue와 유사
    id = Column(Integer, primary_key=True, index=True)
    # Spring의 @Column과 유사
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(String)
    category_id = Column(Integer, nullable=True)  # 복합 FK로 처리
    deadline = Column(TIMESTAMP)
    myjob = Column(Boolean, nullable=False, default=False)
    end_at = Column(TIMESTAMP)
    # Spring의 @CreationTimestamp와 유사
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    deleted_at = Column(TIMESTAMP)

    # 관계 설정
    user = relationship("User", back_populates="works")
    category = relationship("Category", back_populates="works")