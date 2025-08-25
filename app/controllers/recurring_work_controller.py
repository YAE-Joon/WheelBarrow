from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.services.recurring_work_service import RecurringWorkService
from app.schemas.recurring_work_schema import *
from typing import List

router = APIRouter(prefix="/recurring-work", tags=["recurring-work"])


@router.post("/", response_model=RecurringWorkResponse)
def create_recurring_work(
    recurring_work: RecurringWorkCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
  service = RecurringWorkService(db)
  return service.create_recurring_work(recurring_work, user.id)


@router.get("/", response_model=List[RecurringWorkResponse])
def get_recurring_works(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
  service = RecurringWorkService(db)
  return service.get_user_recurring_works(user.id)


@router.put("/{recurring_work_id}", response_model=RecurringWorkResponse)
def update_recurring_work(
    recurring_work_id: int,
    update_data: RecurringWorkUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
  service = RecurringWorkService(db)
  try:
    return service.update_recurring_work(recurring_work_id, user.id,
                                         update_data)
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{recurring_work_id}", response_model=RecurringWorkResponse)
def delete_recurring_work(
    recurring_work_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
  service = RecurringWorkService(db)
  try:
    return service.delete_recurring_work(recurring_work_id, user.id)
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# app/schedulers/recurring_work_scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.core.database import SessionLocal
from app.services.recurring_work_service import RecurringWorkService
import logging

logger = logging.getLogger(__name__)


def execute_recurring_works():
  """반복 작업 실행"""
  try:
    db = SessionLocal()
    service = RecurringWorkService(db)
    service.execute_pending_recurring_works()
    logger.info("Recurring works executed successfully")
  except Exception as e:
    logger.error(f"Error executing recurring works: {e}")
  finally:
    db.close()


def start_recurring_work_scheduler():
  """반복 작업 스케줄러 시작"""
  scheduler = BackgroundScheduler()

  # 매 시간마다 실행 (실제로는 더 자주 실행하거나 cron 형태로 설정 가능)
  trigger = IntervalTrigger(hours=12)
  scheduler.add_job(execute_recurring_works, trigger, id='recurring_works')

  scheduler.start()
  logger.info("Recurring work scheduler started")

  return scheduler