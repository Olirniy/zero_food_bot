from sqlalchemy.orm import Session
from models.dish import Dish


def get_dish_by_id(db: Session, dish_id: int) -> Dish:
    return db.query(Dish).filter(Dish.id == dish_id).first()


def get_dishes_by_category(db: Session, category_id: int) -> list[Dish]:
    return db.query(Dish).filter(Dish.category_id == category_id).all()


def create_dish(
    db: Session,
    category_id: int,
    name: str,
    description: str,
    price: float,
    image_url: str = None
):
    db_dish = Dish(
        category_id=category_id,
        name=name,
        description=description,
        price=price,
        image_url=image_url
    )
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish








# from typing import List, Optional, TYPE_CHECKING
#
# if TYPE_CHECKING:
#     from storage.dish_storage import DishStorage
#     from models.dish import Dish
#
# class DishRepository:
#     def __init__(self, storage: 'DishStorage') -> None:
#         self._storage: 'DishStorage' = storage
#
#     def get_by_category(self, category_id: int) -> List['Dish']:
#         pass
#
#     def get_by_id(self, id: int) -> Optional['Dish']:
#         pass
#
#     def create_bulk(self, dishes: List['Dish']) -> None:
#         pass