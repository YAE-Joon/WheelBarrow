from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.work_schema import *
from app.core.deps import *
from app.services.work_service import WorkService
from app.models.user import User
from typing import List

router = APIRouter(prefix="/work", tags=["work"])

@router.post("/",response_model=WorkResponse)
def create_work(    
    work: WorkCreate,
    user: User = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    service = WorkService(db)
    work.user_id = user.id
    print("work: ",work.user_id,type(work.user_id))
    return service.create_work(work)

@router.get("/today",response_model = List[TodayWorkResponse])
def get_today_works(
    user: User = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    service = WorkService(db)
    user_id = user.id
    return service.get_today_works(user_id)

@router.put("/work/{work_id}", response_model=WorkEdit)
def put_today_work(
    work_id: int,
    work: WorkPut,
    user: User = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    service = WorkService(db)
    user_id = user.id
    return service.put_today_work(user_id,work_id,work)

@router.put("/end/{work_id}",response_model=WorkEdit)
def end_work(
    work_id: int,
    user: User = Depends(get_current_user),
    db : Session = Depends(get_db)
):  
    service = WorkService(db)
    user_id = user.id
    return service.end_work(user_id,work_id)

@router.get("/weekend",response_model = List[EndWorkResponse])
def get_end_works(
    start : datetime,
    end : datetime,
    user: User = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    service = WorkService(db)
    user_id = user.id
    return service.get_end_works(user_id,start,end)

@router.put("/delete/{work_id}",response_model= WorkResponse)
def delete_work(
    work_id: int,
    user: User = Depends(get_current_user),
    db : Session = Depends(get_db)
):
  service = WorkService(db)
  user_id = user.id
  return service.delete_work(user_id,work_id)