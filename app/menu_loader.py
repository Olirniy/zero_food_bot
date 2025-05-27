import json
from typing import List, Dict

from repository.category_repo import CategoryRepository
from repository.dish_repo import DishRepository
from models.category import Category
from models.dish import Dish


class MenuLoader:
    def __init__(
        self,
        category_repository: 'CategoryRepository',
        dish_repository: 'DishRepository'
    ) -> None:
        self._category_repository: 'CategoryRepository' = category_repository
        self._dish_repository: 'DishRepository' = dish_repository

    def load_menu(self, file_path: str) -> None:
        """
        Load a menu from a JSON file and replace existing data.

        Opens the JSON file at `file_path`, which should contain two top-level keys:
        - "categories": a list of objects with "id" (int) and "name" (str)
        - "dishes": a list of objects with keys:
            "id" (int), "category_id" (int), "name" (str),
            "short_description" (str), "description" (str),
            "price" (float or str), and optional "photo_url" (str)

        Deletes all existing categories and dishes, then creates new ones.
        """
        # Read and parse the JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            data: Dict = json.load(f)

        # 1. Remove old menu
        self._category_repository.del_all()
        self._dish_repository.del_all()

        # 2. Create categories
        categories_data: List[Dict] = data.get("categories", [])
        for cat_data in categories_data:
            category = Category(
                id=cat_data["id"],
                name=cat_data["name"]
            )
            self._category_repository.create(category)

        # 3. Create dishes
        dishes_data: List[Dict] = data.get("dishes", [])
        dish_list: List['Dish'] = []
        for dish_data in dishes_data:
            dish = Dish(
                id=dish_data["id"],
                category_id=dish_data["category_id"],
                name=dish_data["name"],
                short_description=dish_data["short_description"],
                description=dish_data["description"],
                price=float(dish_data["price"]),
                photo_url=dish_data.get("photo_url")
            )
            dish_list.append(dish)
        self._dish_repository.add_bulk(dish_list)
