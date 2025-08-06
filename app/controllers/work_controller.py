from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.work_schema import WorkCreate,WorkResponse,TodayWorkResponse,WorkPut
from app.services.work_service import WorkService
from typing import List

router = APIRouter(prefix="/work", tags=["work"])

@router.post("/",response_model=WorkResponse)
def create_work(    
    work: WorkCreate,
    db : Session = Depends(get_db)
):
    service = WorkService(db)
    work.user_id = 1
    return service.create_work(work)

@router.get("/today",response_model = List[TodayWorkResponse])
def get_today_works(
    db : Session = Depends(get_db)
):
    service = WorkService(db)
    user_id = 1
    return service.get_today_works(user_id)

@router.put("/work/{work_id}", response_model=TodayWorkResponse)
def put_today_work(
    work_id: int,
    work: WorkPut,
    db : Session = Depends(get_db)
):
    service = WorkService(db)
    user_id = 1
    return service.put_today_work(user_id,work_id,work)