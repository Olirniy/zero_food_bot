
# repository/dish_repo.py

from models.dish import Dish
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from storage.dish_storage import DishStorage

class DishRepository:
    def __init__(self, storage: 'DishStorage') -> None:
        self._storage: 'DishStorage' = storage
        self._dishes: List['Dish'] = self._storage.load_all()

    def del_all(self) -> None:
        self._storage.del_all()
        self._dishes = []

    def add_bulk(self, dishes: List['Dish']) -> None:
        self._dishes.extend(dishes)
        self._storage.save_all(self._dishes)

    def get_by_category(self, category_id: int) -> List['Dish']:
        """
        Retrieve all dishes matching the given category_id.
        """
        return [dish for dish in self._dishes if dish.category_id == category_id]

    def get_by_id(self, id: int) -> Optional['Dish']:
        """
        Retrieve a single dish by its id.
        """
        for dish in self._dishes:
            if dish.id == id:
                return dish
        return None

    def create_test_dishes(self) -> None:
        self._dishes = [
            Dish(
                id=1,
                category_id=1,
                name="Греческий салат «Афины»",
                short_description="Освежающий микс овощей с брынзой и оливками",
                description="Хрустящие огурцы и помидоры...",
                price=450,
                photo_url="images/salads/Greek salad Athens/01.png"
            ),
            Dish(
                id=2,
                category_id=1,
                name="Салат с печёной свёклой и козьим сыром",
                short_description="Нежная свёкла и пикантный сыр на подушке рукколы",
                description="Запечённая до карамелизации свёкла на свежей рукколе...",
                price=520,
                photo_url="images/salads/Salad with roasted beetroot and goat's cheese/01.png"
            )
        ]

