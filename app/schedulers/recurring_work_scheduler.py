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
  trigger = IntervalTrigger(hours=1)
  scheduler.add_job(execute_recurring_works, trigger, id='recurring_works')

  scheduler.start()
  logger.info("Recurring work scheduler started")

  return scheduler