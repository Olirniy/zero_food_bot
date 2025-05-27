from typing import Any

from config import SQL_DATA
from storage.category_storage import CategoryStorage
from storage.dish_storage import DishStorage
from storage.db_session import DBSession
from storage.feedback_storage import FeedbackStorage
from storage.order_items_storage import OrderItemStorage
from storage.order_storage import OrderStorage


def init_storage(db_session: DBSession) -> dict[str, Any]:
    category_storage = CategoryStorage(db_session, SQL_DATA)
    dish_storage = DishStorage(db_session, SQL_DATA)
    feedback_storage = FeedbackStorage(db_session, SQL_DATA)
    order_item_storage = OrderItemStorage(db_session, SQL_DATA)
    order_storage = OrderStorage(db_session, SQL_DATA)

    return {
        "category_storage": category_storage,
        "dish_storage": dish_storage,
        "feedback_storage": feedback_storage,
        "order_item_storage": order_item_storage,
        "order_storage": order_storage
    }