import jwt
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy_orm.session import Session
from app.models.user import User
from app.core.database import get_db
from app.core.security import decode_jwt
from app.services.auth_service import AuthService

#OAuth2 스키마 정의(토큰 URL 지정)- 어디에서 토큰이 발행되는지 url을 표시하는 것임.
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_auth_service(db: Session = Depends(get_db))->AuthService:
  return AuthService(db)
#
async def get_current_user(
    token: str = Depends(oauth2_schema),
    auth_service: AuthService = Depends(get_auth_service)
    ) -> User:
  credentials_exception = HTTPException(
      status_code = status.HTTP_401_UNAUTHORIZED,
      detail = "Could not validate credentials",
      headers = {"WWW-Authenticate": "Bearer"},
  )

  try:
    payload = decode_jwt(token)
    if not payload:
      raise credentials_exception
    user_id = payload.get("sub")
    token_type = payload.get("type")

    if user_id is None or token_type != "access":
      raise credentials_exception

  except Exception:
    raise credentials_exception

  return auth_service.get_user(user_id)