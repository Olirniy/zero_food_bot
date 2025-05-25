import sys
from pathlib import Path
import pytest
import os
import sqlite3
from datetime import datetime
from storage.db_session import DBSession
from models.user import User
from models.dish import Dish
from models.order import Order
from config import SQL_DATA

# Добавляем корень проекта в пути Python
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope="session")
def test_db_path(tmp_path_factory):
    """Фикстура для временной тестовой БД."""
    path = tmp_path_factory.mktemp("data") / "test.db"
    # Переопределяем путь к БД для тестов
    SQL_DATA["db_path"] = str(path)
    yield path
    # pytest автоматически удалит временные файлы


@pytest.fixture
def db(test_db_path):
    """Фикстура с полной изоляцией тестов"""
    # Убедимся, что предыдущее соединение закрыто
    db = DBSession()
    db.close()  # Используем ваш существующий метод close()

    # Удаляем старую БД если существует
    if os.path.exists(test_db_path):
        try:
            os.unlink(test_db_path)
        except PermissionError:
            pass

    # Создаем новую БД
    db = DBSession()

    # Создаем таблицы
    with db.get_session() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                username TEXT
            );
            CREATE TABLE IF NOT EXISTS dishes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                short_description TEXT,
                description TEXT,
                price REAL NOT NULL,
                photo_url TEXT
            );
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                payment_method TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                dish_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL
            );
        """)
        conn.commit()

    yield db

    # Закрываем соединение
    db.close()




@pytest.fixture
def sample_user():
    return User(id=0, telegram_id=12345, username="test_user")


@pytest.fixture
def sample_dish(db):
    """Фикстура создает тестовое блюдо в изолированной БД"""
    dish = Dish(
        id=0,
        category_id=1,
        name="TEST_DISH_FOR_ORDER_ITEMS",
        short_description="Для теста",
        description="Только для теста order_items",
        price=10.0,
        photo_url="test.jpg"
    )
    from storage.dish_storage import DishStorage
    dish_storage = DishStorage(db, SQL_DATA)
    return dish_storage.save(dish)


@pytest.fixture
def sample_order(db, sample_user):
    """Фикстура создает тестовый заказ"""
    from storage.user_storage import UserStorage
    from storage.order_storage import OrderStorage
    from models.enums import OrderStatus  # Добавляем импорт

    # Сначала сохраняем пользователя
    user_storage = UserStorage(db, SQL_DATA)
    saved_user = user_storage.save(sample_user)

    # Затем создаем заказ с правильным enum-значением
    order = Order(
        id=0,
        user_id=saved_user.id,
        status=OrderStatus.IN_CART,  # Используем enum вместо строки
        payment_method=None,
        created_at=datetime.now()
    )
    order_storage = OrderStorage(db, SQL_DATA)
    return order_storage.save(order)


@pytest.fixture(autouse=True)
def clean_tables(db):
    """Автоматически очищает таблицы перед каждым тестом"""
    with db.get_session() as conn:
        # Отключаем foreign keys для очистки
        conn.execute("PRAGMA foreign_keys = OFF")
        conn.execute("DELETE FROM order_items")
        conn.execute("DELETE FROM orders")
        conn.execute("DELETE FROM dishes")
        conn.execute("DELETE FROM users")
        # Включаем foreign keys обратно
        conn.execute("PRAGMA foreign_keys = ON")
        conn.commit()
    yield