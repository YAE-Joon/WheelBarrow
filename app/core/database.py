from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Iterator

from app.core.config import settings

# 환경변수 로드(Spring의 application.properties와 유사)


# 데이터베이스 URL 설정 (Spring의 spring.datasource.url과 유사)
engine = create_engine(
  settings.database_url
)
# SQLAlchemy 엔진 생성 (Spring의 DataSource와 유사)
# 세션 로컬 클래스 생성 (Spring의 EntityManager와 유사)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성 (JPA의 @Entity 상속용)
Base = declarative_base()

def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔥 모든 모델을 import해서 SQLAlchemy가 인식하도록 함
from app.models import User, Category, Work, RecurringWork
