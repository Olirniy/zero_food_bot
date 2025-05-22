from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)



#from models.base import Base  # Импортируйте все модели

# def init_db():
#     engine = create_engine('sqlite:///foodbot.db')
#     Base.metadata.create_all(engine)  # Создаст только недостающие таблицы
#     return engine

# 1. Сначала создаем базовый класс
Base = declarative_base()

# 2. Настройка подключения
engine = create_engine('sqlite:///foodbot.db', echo=True)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """Явная инициализация всех таблиц"""
    try:
        # 3. Импорт ВСЕХ моделей ПОСЛЕ создания Base
        from models.user import User
        from models.category import Category
        from models.dish import Dish

        # 4. Создаем таблицы
        Base.metadata.create_all(bind=engine)

        # Проверка
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Созданные таблицы: {tables}")

        if 'users' not in tables:
            raise RuntimeError("Таблица users не создана!")

    except Exception as e:
        logger.critical(f"Ошибка инициализации БД: {e}")
        raise

# def init_db():
#     """Безопасная инициализация всех необходимых таблиц"""
#     try:
#         from models.user import User
#         from models.category import Category
#
#         inspector = inspect(engine)
#
#         # Всегда пытаемся создать все таблицы
#         Base.metadata.create_all(engine)
#         logger.info("Таблицы успешно созданы или уже существуют")
#
#     except Exception as e:
#         logger.critical(f"Ошибка инициализации БД: {e}")
#         raise