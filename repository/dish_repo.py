from typing import List, Optional, TYPE_CHECKING
from models.dish import Dish

if TYPE_CHECKING:
    from storage.dish_storage import DishStorage

class DishRepository:
    def __init__(self, storage: 'DishStorage'):
        self._storage = storage

    def get_by_id(self, dish_id: int) -> Optional[Dish]:
        """Получить блюдо по ID"""
        return self._storage.load_by_id(dish_id)

    def get_by_category(self, category_id: int) -> List[Dish]:
        """Получить все блюда категории"""
        return self._storage.load_by_category(category_id)

    def create(self, dish: Dish) -> Dish:
        """Добавить новое блюдо"""
        self._storage.save(dish)
        return self._storage.load_by_id(dish.id)

    def create_bulk(self, dishes: List[Dish]) -> None:
        """Массовое добавление блюд"""
        for dish in dishes:
            self._storage.save(dish)








# from typing import List, Optional, TYPE_CHECKING
#
# if TYPE_CHECKING:
#     from storage.dish_storage import DishStorage
#     from models.dish import Dish
#
# class DishRepository:
#     def __init__(self, storage: 'DishStorage') -> None:
#         self._storage = storage
#
#     def get_by_category(self, category_id: int) -> List['Dish']:
#         """Получает все блюда указанной категории"""
#         return self._storage.load_by_category(category_id)
#
#     def get_by_id(self, dish_id: int) -> Optional['Dish']:
#         """Получает блюдо по ID"""
#         return self._storage.load_by_id(dish_id)
#
#     def create_bulk(self, dishes: List['Dish']) -> None:
#         """Массовое добавление блюд"""
#         for dish in dishes:
#             self._storage.save(dish)