from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging

logger = logging.getLogger(__name__)

# 1. Сначала создаем базовый класс
SqlAlchemyBase = declarative_base()

# 2. Затем подключаемся к БД
engine = create_engine('sqlite:///foodbot.db', echo=True)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """Инициализация всех таблиц"""
    try:
        # 3. Импортируем модели ПОСЛЕ создания SqlAlchemyBase
        from models import User

        # 4. Создаем таблицы
        SqlAlchemyBase.metadata.create_all(engine)
        logger.info("Таблицы успешно созданы")
    except Exception as e:
        logger.critical(f"Ошибка создания таблиц: {e}")
        raise