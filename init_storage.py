from storage.db_session import DBSession
from storage.user_storage import UserStorage
from storage.category_storage import CategoryStorage
from storage.dish_storage import DishStorage
from config import SQL_DATA

def init_storage(db_session: DBSession) -> dict:
    """Инициализирует все storage-классы"""
    return {
        'user_storage': UserStorage(db_session, SQL_DATA),
        'category_storage': CategoryStorage(db_session, SQL_DATA),
        'dish_storage': DishStorage(db_session, SQL_DATA)
    }