import pytest
from storage.user_storage import UserStorage
from models.user import User
from config import SQL_DATA

def test_user_operations(db):
    storage = UserStorage(db, SQL_DATA)

    # Тест создания
    user = User(id=0, telegram_id=99999, username="test_user")
    storage.save(user)
    assert user.id > 0

    # Тест загрузки
    loaded_user = storage.load_by_telegram_id(99999)
    assert loaded_user is not None
    assert loaded_user.username == "test_user"