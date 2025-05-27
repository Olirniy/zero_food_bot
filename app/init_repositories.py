from typing import TYPE_CHECKING, Any

from app.menu_loader import MenuLoader
from repository.category_repo import CategoryRepository
from repository.feedback_repo import FeedbackRepository
from repository.order_item_repo import OrderItemRepository
from repository.order_repo import OrderRepository

if TYPE_CHECKING:
    from app.bot import ZeroFoodBot
from repository.dish_repo import DishRepository


def init_repositories(bot: 'ZeroFoodBot', storage_list: dict[str, Any]) -> None:
    # Инициализация хранилища блюд
    category_storage = storage_list["category_storage"]
    dish_storage = storage_list["dish_storage"]
    feedback_storage = storage_list["feedback_storage"]
    order_items_storage = storage_list["order_item_storage"]
    order_storage = storage_list["order_storage"]

    # Создание репозитория блюд
    bot.set_category_repository(CategoryRepository(category_storage))
    bot.set_dish_repository(DishRepository(dish_storage))
    bot.set_feedback_repository(FeedbackRepository(feedback_storage))
    bot.set_order_item_repository(OrderItemRepository(order_items_storage))
    bot.set_order_repository(OrderRepository(order_storage, bot.get_order_item_repository()))

    #загрузчик меню из файла
    bot.menu_loader = MenuLoader(bot.get_category_repository(), bot.get_dish_repository())