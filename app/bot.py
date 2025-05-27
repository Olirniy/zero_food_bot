from telebot import TeleBot
from typing import Any, Dict,Optional

from app.menu_loader import MenuLoader
from builders.category_menu_builder import CategoryMenuBuilder
from repository.category_repo import CategoryRepository
from repository.dish_repo import DishRepository
from repository.feedback_repo import FeedbackRepository
from repository.order_item_repo import OrderItemRepository
from repository.order_repo import OrderRepository


class ZeroFoodBot(TeleBot):
    def __init__(self, token):
        super().__init__(token)
        #репозитории
        self._category_repository: Optional[CategoryRepository] = None  # type: ignore
        self._dish_repository: Optional[DishRepository] = None
        self._feedback_repository: Optional[FeedbackRepository] = None
        self._order_repository: Optional[OrderRepository] = None
        self._order_item_repository: Optional[OrderItemRepository] = None
        #билдеры
        self._category_menu_builder: Optional[CategoryMenuBuilder] = None
        #загрузчики информации из файлов
        self._menu_loader: Optional[MenuLoader] = None

    def set_category_repository(self, repository: CategoryRepository) -> None:
        """
        Сохраняет репозиторий категорий в контексте бота.
        """
        self._category_repository = repository
        self._category_menu_builder = CategoryMenuBuilder(repository)

    def get_category_repository(self) -> CategoryRepository | None:
        """
        Возвращает ранее сохранённый репозиторий категорий.
        """
        return self._category_repository
    
    def set_dish_repository(self, repo: DishRepository) -> None:
        self._dish_repository = repo

    def get_dish_repository(self) -> DishRepository | None:
        return self._dish_repository

    def set_feedback_repository(self, repo: 'FeedbackRepository') -> None:
        self._feedback_repository = repo

    def get_feedback_repository(self) -> FeedbackRepository | None:
        return self._feedback_repository

    def set_order_repository(self, repo: 'OrderRepository') -> None:
        self._order_repository = repo

    def get_order_repository(self) -> OrderRepository | None:
        return self._order_repository

    def set_order_item_repository(self, repo: 'OrderItemRepository') -> None:
        self._order_item_repository = repo

    def get_order_item_repository(self) -> OrderItemRepository | None:
        return self._order_item_repository

    @property
    def category_menu_builder(self) -> CategoryMenuBuilder | None:
        return self._category_menu_builder

    @property
    def menu_loader(self) -> MenuLoader | None:
        return self._menu_loader

    @menu_loader.setter
    def menu_loader(self, loader: MenuLoader) -> None:
        self._menu_loader = loader