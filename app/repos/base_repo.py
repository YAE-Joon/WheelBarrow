from sqlalchemy_orm.session import Session


class BaseRepository:

  def __init__(self, db: Session):
    self.db = db


  def get_active_query(self, model):
    """삭제되지 않은 레코드만 조회하는 기본 쿼리"""
    return self.db.query(model).filter(
        model.deleted_at.is_(None)
    )
