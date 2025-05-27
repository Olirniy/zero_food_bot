from typing import List
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from repository.category_repo import CategoryRepository
from models.category import Category

class CategoryMenuBuilder:
    def __init__(self, repository: CategoryRepository) -> None:
        self._repository: CategoryRepository = repository

    def build_menu(self) -> InlineKeyboardMarkup:
        """
        Загружает все категории из репозитория и собирает кнопки в клавиатуру.
        """
        categories: List[Category] = self._repository.get_all()
        markup = InlineKeyboardMarkup(row_width=2)

        buttons = [
            InlineKeyboardButton(
                text=category.name,
                callback_data=f"category_select:{category.id}"
            )
            for category in categories
        ]
        markup.add(*buttons)
        return markup
