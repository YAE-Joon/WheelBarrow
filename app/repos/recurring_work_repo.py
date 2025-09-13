from app.models.recurringWork import RecurringWork
from app.repos.base_repo import BaseRepository
from datetime import datetime
from typing import Optional,List

class RecurringWorkRepository(BaseRepository):

  def create(self, recurrent_work_data: dict) -> RecurringWork:
    db_recurring_work = RecurringWork(**recurrent_work_data)
    self.db.add(db_recurring_work)
    self.db.commit()
    self.db.refresh(db_recurring_work)
    return db_recurring_work

  def get_by_user_id(self, user_id: int) -> List[RecurringWork]:
    return self.get_active_query(RecurringWork).filter(RecurringWork.user_id== user_id).all()

  def get_pending_executions(self, current_time : datetime) -> List[RecurringWork]:
    return self.get_active_query(RecurringWork).filter(
        RecurringWork.is_active == True,
        RecurringWork.next_execution_date<= current_time
      ).all()

  def update_next_execution_date(self, recurring_work_id : int , next_date : datetime , next_start_date : datetime , next_deadline : datetime) -> datetime:
    recurring_work = self.get_active_query(RecurringWork).filter(
        RecurringWork.id == recurring_work_id,
    ).first()

    if recurring_work:
      recurring_work.next_execution_date = next_date
      recurring_work.started_at = next_start_date
      recurring_work.deadline = next_deadline
      self.db.commit()
      self.db.refresh(recurring_work)

    return recurring_work

  def update(self, recurrent_work_id : int, user_id : int, update_data : dict) -> Optional[RecurringWork]:
    recurrent_work = self.get_active_query(RecurringWork).filter(
        RecurringWork.id == recurrent_work_id,
        RecurringWork.user_id == user_id,
    ).first()
    if not recurrent_work:
      raise ValueError('Recurring work not found')

    for key, value in update_data.items():
      if hasattr(recurrent_work, key) and value is not None:
        setattr(recurrent_work, key, value)

    self.db.commit()
    self.db.refresh(recurrent_work)
    return recurrent_work

  def get_by_recurring_work_id(self, recurring_work_id: int, user_id: int) -> Optional[RecurringWork]:
    recurrent_work = self.get_active_query(RecurringWork).filter(
        RecurringWork.id == recurring_work_id,
        RecurringWork.user_id == user_id
    ).first()
    if not recurrent_work:
      raise ValueError('Recurring work not found')
    return recurrent_work

  def delete(self, recurrent_work_id: int,user_id: int) -> None:
    today = datetime.today()
    recurrent_work = self.get_active_query(RecurringWork).filter(
        RecurringWork.id == recurrent_work_id,
        RecurringWork.user_id == user_id,
        RecurringWork.deleted_at.is_(None)
    ).first()
    if not recurrent_work:
      raise ValueError('Recurring work not found')
    recurrent_work.deleted_at = today
    self.db.commit()
    # self.db.refresh(recurrent_work)
    return None