from sqlalchemy.orm import Session
from storage.db import SessionLocal
from models.user import User



def user_exists(telegram_id: int) -> bool:
    with SessionLocal() as session:
        return session.query(User).filter(User.telegram_id == telegram_id).first() is not None

def add_user(user: User):
    if not user_exists(user.telegram_id):
        with SessionLocal() as session:
            session.add(user)
            session.commit()

