from sqlalchemy.orm import Session
from storage.db import SessionLocal
import logging


logger = logging.getLogger(__name__)
from repository.dish_repo import (
    get_dish_by_id,
    get_dishes_by_category,
    create_dish
)




def add_dish(
    name: str,
    description: str,
    price: float,
    category_id: int,
    image_url: str = None
):
    with SessionLocal() as session:
        try:
            # Явное преобразование типов
            dish_data = {
                'name': str(name),
                'description': str(description) if description else None,
                'price': float(price),
                'category_id': int(category_id),
                'image_url': str(image_url) if image_url else None
            }
            return create_dish(session, **dish_data)
        except Exception as e:
            session.rollback()
            logger.error(f"Dish creation failed: {e}")
            raise


# def get_dishes_with_categories():
#     """Получить все блюда с информацией о категориях"""
#     with SessionLocal() as session:
#         try:
#             from repository.dish_repo import get_dishes_with_categories as repo_get_dishes_with_categories
#             return repo_get_dishes_with_categories(session)
#         except Exception as e:
#             logger.error(f"Error getting dishes with categories: {e}")
#             raise

def get_dishes_by_category(category_id: int):
    """Получить блюда по ID категории"""
    with SessionLocal() as session:
        try:
            from repository.dish_repo import get_dishes_by_category as repo_get_dishes
            return repo_get_dishes(session, category_id)
        except Exception as e:
            logger.error(f"Error getting dishes by category: {e}")
            raise


def get_all_dishes_with_categories():
    """Получить все блюда с информацией о категориях"""
    with SessionLocal() as session:
        try:
            from repository.dish_repo import get_all_dishes_with_categories as repo_get_all_dishes
            return repo_get_all_dishes(session)
        except Exception as e:
            logger.error(f"Error getting all dishes with categories: {e}")
            raise



# def add_dish(
#     name: str,
#     description: str,
#     price: float,
#     image_url: str = None,
#     category_id: int = None
# ):
#     with SessionLocal() as session:
#         return create_dish(
#             session,
#             name=name,
#             description=description,
#             price=price,
#             image_url=image_url,
#             category_id=category_id
#         )

def get_dish(dish_id: int):
    with SessionLocal() as session:
        return get_dish_by_id(session, dish_id)

def get_all_dishes_by_category(category_id: int) -> list:
    with SessionLocal() as session:
        return get_dishes_by_category(session, category_id)










# from typing import List, Optional, TYPE_CHECKING
#
# if TYPE_CHECKING:
#     from storage.db_session import DBSession
#     from models.dish import Dish
#
# class DishStorage:
#     def __init__(self, db_session: 'DBSession', sql_data: dict[str, str]) -> None:
#         self._db_session = db_session
#         self._sql_data = sql_data
#         self._init_table()
#
#     def _init_table(self) -> None:
#         pass
#
#     def save(self, dish: 'Dish') -> None:
#         pass
#
#     def load_by_id(self, id: int) -> Optional['Dish']:
#         pass
#
#     def load_by_category(self, category_id: int) -> List['Dish']:
#         pass