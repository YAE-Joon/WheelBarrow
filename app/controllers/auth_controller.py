from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth_schema import UserCreate, UserResponse, Token

# Spring의 @RestController와 동일한 역할
# @RequestMapping("/users")와 유사

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Spring의 @PostMapping과 동일
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user : UserCreate,
    db: Session = Depends(get_db)
):
    service = AuthService(db)
    try:
         return service.create_user(user)
    except ValueError as e :
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
  """로그인 엔드포인트(OAuth2호환)"""
  auth_service = AuthService(db)

  #OAuth2PasswordRequestForm은 username 필드를 사용
  user = auth_service.authenticate_user(form_data.username, form_data.password)
  if not user:
      raise HTTPException(
          status_code = status.HTTP_401_UNAUTHORIZED,
          detail = "Incorrect username or password",
          headers = {"WWW-Authenticate": "Bearer"},
      )

  tokens = auth_service.create_tokens(user)
  return  tokens