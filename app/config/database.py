import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


# 환경변수 로드(Spring의 application.properties와 유사)
load_dotenv()

# 데이터베이스 URL 설정 (Spring의 spring.datasource.url과 유사)
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy 엔진 생성 (Spring의 DataSource와 유사)
engine = create_engine(DATABASE_URL)


# 세션 로컬 클래스 생성 (Spring의 EntityManager와 유사)
SessionLocal = sessionmaker (autocommit = False,autoFlush=False, bind=engine)

#Base 클래스 생성 (JPA의 @Entity 상속용)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()