from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from typing import Optional

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

  class Config:
    env_file = ".env"
    extra = "ignore"

settings = Settings()