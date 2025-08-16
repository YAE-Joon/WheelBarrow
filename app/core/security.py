from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from passlib.context import CryptContext

from app.core.config import settings

#패스워드 해싱 컨텍스트 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
  """평문 패스워드와 해시된 패스워드 비교"""
  return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
  """패스워드 해싱"""
  return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None)-> str:
  """엑세스 토큰 생성"""
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

  to_encode.update({"exp": expire, "type": "access"})
  encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm= settings.jwt_algorithm)

  return encoded_jwt

def create_refresh_token(data:dict, expires_delta: Optional[timedelta] = None) -> str:
  """리프레시 토큰 생성"""
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.refresh_token_expire_days)

  to_encode.update({"exp": expire, "type": "refresh"})

  encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm= settings.jwt_algorithm)
  return encoded_jwt

def decode_jwt(token: str) -> dict:
  """jwt 토큰 디코드"""
  try:
    payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    return payload
  except jwt.ExpiredSignatureError:
    return {}
  except jwt.InvalidTokenError:
    return {}