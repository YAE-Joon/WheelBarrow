from pydantic_setting import BaseSettings
from tpying import Optional
import os

class Settings(BaseSettings):
    # 데이터베이스 설정
    db_host:str
    db_port:int
    db_user:str
    db_password:str
    db_name:str
    database_url:Optional[str] = None

    #애플리케이션 설정
    debug: bool
    secret_key : str

    class Config:
        env_file =".env"
        case_sensitive = False
        #.env 없으면 에러발생
        env_file_encoding = 'utf-8'

    @property
    def db_url(self) ->str:
        """DATABASE_URL이 있으면 우선 사용, 없으면 개별 설정으로 구성"""
        if self.database_url:
            return self.database_url
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
#전역 인스턴스
settings = Settings()