import os
import sys
from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context

# 현재 파일의 상위 디렉토리(app)를 Python 경로에 추가
current_path = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.dirname(current_path)
sys.path.insert(0, app_path)

# 이제 app 디렉토리 기준으로 import 가능
from config.database import Base
from core.config import settings

# Alembic Config 객체
config = context.config

# Python 로깅 설정
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 메타데이터 설정 - 모든 모델이 여기에 포함됨
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """오프라인 모드에서 마이그레이션 실행"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """온라인 모드에서 마이그레이션 실행"""
    # 데이터베이스 연결 생성
    connectable = create_engine(settings.db_url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# 오프라인/온라인 모드 분기
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
