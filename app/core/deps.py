from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

#OAuth2 스키마 정의(토큰 URL 지정)
oath2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
#
# async def get_current_user(
#     token: str = Depends(oath2_schema),
#     ):
#   try:
#     payload = token
