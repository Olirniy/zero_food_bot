from storage.db_session import DBSession
from storage.user_storage import UserStorage
from storage.category_storage import CategoryStorage
from storage.dish_storage import DishStorage
from config import SQL_DATA
from storage.order_storage import OrderStorage
from storage.order_items_storage import OrderItemStorage


def init_storage(db_session: DBSession) -> dict:
    return {
        'user_storage': UserStorage(db_session, SQL_DATA),
        'category_storage': CategoryStorage(db_session, SQL_DATA),
        'dish_storage': DishStorage(db_session, SQL_DATA),
        'order_storage': OrderStorage(db_session, SQL_DATA),
        'order_items_storage': OrderItemStorage(db_session, SQL_DATA)
    }