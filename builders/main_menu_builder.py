from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import ADMINS


class MainMenuBuilder:
    def __init__(self) -> None:
        pass

    @staticmethod
    def build_menu(user_id) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Показать меню", callback_data='cmd_:show_menu'))
        keyboard.add(InlineKeyboardButton("Показать корзину", callback_data="cmd_:show_cart"))
        keyboard.add(InlineKeyboardButton("Очистить корзину", callback_data="cmd_:clear_cart"))
        keyboard.add(InlineKeyboardButton("Показать список заказов", callback_data="cmd_:show_orders"))
        keyboard.add(InlineKeyboardButton("Оставить отзыв", callback_data="cmd_:add_feedback"))
        if user_id in ADMINS:
            keyboard.add(InlineKeyboardButton("Показать отзывы", callback_data="cmd_:show_feedbacks"))
            keyboard.add(InlineKeyboardButton("Загрузить новое меню", callback_data="cmd_:load_menu"))
            keyboard.add(InlineKeyboardButton("Изменить статус заказа", callback_data="cmd_:change_order_status"))
        return keyboard
