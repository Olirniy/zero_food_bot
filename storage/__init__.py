# Для storage/__init__.py
from .category_storage import get_all_categories, add_category
from .dish_storage import add_dish, get_all_dishes_by_category

__all__ = ['get_all_categories', 'add_category', 'add_dish', 'get_all_dishes_by_category']