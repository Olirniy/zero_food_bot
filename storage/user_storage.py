from sqlalchemy.orm import Session
from storage.db import SessionLocal
from models.user import User
import logging
logger = logging.getLogger(__name__)



def user_exists(telegram_id: int) -> bool:
    with SessionLocal() as session:
        return session.query(User).filter(User.telegram_id == telegram_id).first() is not None


def add_user(user: User):
    if not user_exists(user.telegram_id):
        with SessionLocal() as session:
            session.add(user)
            session.commit()


def get_user_by_telegram_id(telegram_id: int):
    with SessionLocal() as session:
        try:
            from repository.user_repo import get_user_by_telegram_id as repo_get_user
            return repo_get_user(session, telegram_id)
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None

