import os
from typing import List

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
  # Spring의 application properties와 유사

  #App
  app_name : str = "Wheel Barrow"
  debug: bool = False
  #database url
  database_url: str

  #Security
  secret_key: str
  access_token_expire_minutes: int = 30
  refresh_token_expire_days: int = 30
  jwt_secret_key: str
  jwt_algorithm: str

  # === AWS 배포를 위한 서버설정 ===
  host: str = "0.0.0.0"# Docker 컨테이너에서 외부 접근 허용
  port: int = 8000     # FastAPI 기본포트
  reload: bool = False # 운영환경 auto-reload 비활성화

  # === CORS 설정 (프론트 연동)===
  cors_origins: List[str] = ["*"]

  # === 로깅 설정 ===
  log_level: str = "INFO"

  # ===환경 구분용 ===
  environment: str = "development"
  class Config:
    env_file = ".env"
    extra = "ignore"

#함수 결과를 메모리에 캐시해서 같은 함수가 다시 호출될 때 계산하지 않고 캐시된 결과를 반환
@lru_cache
def get_settings() -> Settings:
  return Settings()
settings = get_settings()
