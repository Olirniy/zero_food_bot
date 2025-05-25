import pytest
from models.user import User
from storage.user_storage import UserStorage
from config import SQL_DATA


def test_user_storage_save_returns_user(db):
    """Тест проверяет, что метод save() возвращает сохраненного пользователя"""
    storage = UserStorage(db, SQL_DATA)

    # Создаем тестового пользователя
    test_user = User(id=0, telegram_id=12345, username="test_user")

    # Сохраняем пользователя
    saved_user = storage.save(test_user)

    # Проверяем результаты
    assert saved_user is not None, "Метод save() вернул None"
    assert saved_user.id > 0, "ID пользователя не был установлен"
    assert saved_user.telegram_id == test_user.telegram_id
    assert saved_user.username == test_user.username


def test_user_storage_load_by_telegram_id(db):
    """Тест проверяет загрузку пользователя по telegram_id"""
    storage = UserStorage(db, SQL_DATA)

    # Создаем и сохраняем тестового пользователя
    test_user = User(id=0, telegram_id=54321, username="another_user")
    storage.save(test_user)

    # Загружаем пользователя
    loaded_user = storage.load_by_telegram_id(54321)

    # Проверяем результаты
    assert loaded_user is not None, "Пользователь не был найден"
    assert loaded_user.id > 0
    assert loaded_user.username == "another_user"