from typing import List, Optional

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from dateutil.relativedelta import relativedelta
from app.models.recurringWork import RecurringWork
from app.enums.recurrenceType import RecurrenceType
from app.enums.work_status import WorkStatus
from app.repos.recurring_work_repo import RecurringWorkRepository
from app.repos.work_repo import WorkRepository
from app.schemas.recurring_work_schema import *
import calendar

class RecurringWorkService:
  def __init__(self, db: Session):
    self.recurring_work_repo = RecurringWorkRepository(db)
    self.work_repo = WorkRepository(db)

  def create_recurring_work(self, recurring_work_data: RecurringWorkCreate, user_id:int,) -> RecurringWorkResponse:
    data = recurring_work_data.model_dump()
    data['user_id'] = user_id
    data['next_execution_date'] = data['started_at']

    recurring_work = self.recurring_work_repo.create(data)
    return RecurringWorkResponse.model_validate(recurring_work)

  def get_user_recurring_works(self, user_id:int) -> List[RecurringWorkResponse]:
    recurring_works = self.recurring_work_repo.get_by_user_id(user_id)
    return [RecurringWorkResponse.model_validate(rw) for rw in recurring_works]

  def update_recurring_work(self, recurring_work_id: int, user_id: int,
      update_data: RecurringWorkUpdate) -> RecurringWorkResponse:
    data = update_data.model_dump(exclude_unset=True)
    recurring_work = self.recurring_work_repo.update(recurring_work_id,
                                                     user_id, data)
    return RecurringWorkResponse.model_validate(recurring_work)

  def delete_recurring_work(self, recurring_work_id: int, user_id: int) -> RecurringWorkResponse:
      recurring_work = self.recurring_work_repo.delete(recurring_work_id, user_id)
      return RecurringWorkResponse.model_validate(recurring_work)

  def execute_pending_recurring_works(self):
    """스케줄러에서 호출되는 메서드 - 실행 예정인 반복 작업들을 처리"""
    current_time = datetime.now()
    pending_works = self.recurring_work_repo.get_pending_executions(
      current_time)

    for recurring_work in pending_works:
      # 종료 날짜 확인
      if recurring_work.end_date and current_time > recurring_work.end_date:
        # 반복 작업 비활성화
        self.recurring_work_repo.update(recurring_work.id,
                                        recurring_work.user_id,
                                        {"is_active": False})
        continue

      # 새로운 Work 생성
      work_data = {
        "title": recurring_work.title,
        "content": recurring_work.content,
        "user_id": recurring_work.user_id,
        "category_id": recurring_work.category_id,
        "myjob": recurring_work.myjob,
        "current_status": WorkStatus.TODO,
        "recurring_work_id": recurring_work.id,
        "started_at": current_time
      }

      self.work_repo.create(work_data)

      # 다음 실행 날짜 계산 및 업데이트
      next_date = self._calculate_next_execution_date(recurring_work)
      if next_date:
        self.recurring_work_repo.update_next_execution_date(recurring_work.id,
                                                            next_date)

  def _calculate_next_execution_date(self, recurring_work: RecurringWork) -> \
  Optional[datetime]:
    """다음 실행 날짜 계산"""
    current_date = recurring_work.next_execution_date

    if recurring_work.recurrence_type == RecurrenceType.DAILY:
      return current_date + timedelta(days=recurring_work.interval_value)

    elif recurring_work.recurrence_type == RecurrenceType.WEEKLY:
      return current_date + timedelta(weeks=recurring_work.interval_value)

    elif recurring_work.recurrence_type == RecurrenceType.MONTHLY:
      return current_date + relativedelta(
        months=recurring_work.interval_value)

    elif recurring_work.recurrence_type == RecurrenceType.YEARLY:
      return current_date + relativedelta(years=recurring_work.interval_value)

    elif recurring_work.recurrence_type == RecurrenceType.CUSTOM:
      # 사용자 정의 로직 (recurrence_config 활용)
      return self._calculate_custom_next_date(recurring_work)

    return None

  def _calculate_custom_next_date(self, recurring_work: RecurringWork) -> \
  Optional[datetime]:
    """사용자 정의 반복 규칙 처리"""
    if not recurring_work.recurrence_config:
      return None

    config = recurring_work.recurrence_config
    current_date = recurring_work.next_execution_date

    # 예: 매주 특정 요일 (1:월요일, 7:일요일)
    if "days_of_week" in config:
      days_of_week = config["days_of_week"]
      next_date = current_date + timedelta(days=1)

      while next_date.weekday() + 1 not in days_of_week:
        next_date += timedelta(days=1)

      return next_date

    # 예: 매월 특정 일
    if "day_of_month" in config:
      day_of_month = config["day_of_month"]
      next_month = current_date.replace(day=1) + relativedelta(months=1)

      # 해당 월의 마지막 날짜 확인
      last_day = calendar.monthrange(next_month.year, next_month.month)[1]
      target_day = min(day_of_month, last_day)

      return next_month.replace(day=target_day)

    return current_date + timedelta(days=recurring_work.interval_value)