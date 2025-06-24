from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate, UserResponse

# Spring의 @RestController와 동일한 역할
# @RequestMapping("/users")와 유사

router = APIRouter(prefix="/users", tags=["users"])

# Spring의 @PostMapping과 동일
@router.post("/", response_model=UserResponse)
def create_user(
    user : UserCreate,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    try:
        return service.create_user(user)
    except ValueError as e : 
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )