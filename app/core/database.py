from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from .config import settings
import logging

#로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#SQLAlchemy 엔진 설정
engine = create_engine(
    settings.db_url,
    #연결 풀 설정
    pool_size=20,       #연결 풀 확인
    max_overflow=0,     #추가 연결 허용 수
    pool_pre_ping=True, #연결 상태 확인
    pool_recycle=300,   #연결 재활용 시간(초)
    echo=settings.debug #SQL 쿼리 로그 출력
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind= engine
)

#베이스 모델 클래스
Base = declarative_base()

def get_db() -> Session:
    """
    데이터베이스 세션 의존성
    Spring Boot의 @Autowired EntityManager와 유사
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    데이터베이스 초기화
    모든 테이블 생성
    """
    try:
        #모든 모델의 테이블 생성
        Base.metadata.create_all(bind=engine)
        logger.info("데이터베이스 테이블이 성공적으로 생성되었습니다.")
    except Exception as e:
        logger.error(f"데이터베이스 초기화 실패: {e}")
        raise

def check_db_connection():
    """
    데이터베이스 연결상태 확인
    """
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            logger.info("데이터베이스 연결 성공!")
            return True
    except Exception as e:
        logger.error(f"데이터베이스 연결 실패:{e}")
        return False