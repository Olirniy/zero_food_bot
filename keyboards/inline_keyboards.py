from typing import List

from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from models.order import Order


def get_dish_keyboard_with_add(dish_id):
    markup = types.InlineKeyboardMarkup()
    btn_details = types.InlineKeyboardButton("Подробнее", callback_data=f"details_{dish_id}")
    btn_add = types.InlineKeyboardButton("В корзину", callback_data=f"add_{dish_id}")
    markup.row(btn_details)
    markup.row(btn_add)
    return markup

def get_dish_keyboard(dish_id):
    markup = types.InlineKeyboardMarkup()
    btn_add = types.InlineKeyboardButton("В корзину", callback_data=f"add_{dish_id}")
    markup.row(btn_add)
    return markup

def get_continue_checkout():
    markup = types.InlineKeyboardMarkup()
    btn_continue = types.InlineKeyboardButton("Продолжить", callback_data="continue_shopping")
    btn_checkout = types.InlineKeyboardButton("Оформить заказ", callback_data="confirm_order")
    markup.row(btn_continue, btn_checkout)
    return markup

def select_payment_method_keyboard(order_id: int):
    markup = types.InlineKeyboardMarkup()
    btn_cash = types.InlineKeyboardButton("Наличные", callback_data=f"select_payment_cash:{order_id}")
    btn_card = types.InlineKeyboardButton("Карта", callback_data=f"select_payment_card:{order_id}")
    markup.row(btn_cash, btn_card)
    return markup

def select_order_to_change_status(orders: List[Order]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text=f"№ {order.id} статус: {order.status.get_name()} сумма: {order.get_sum()}",
            callback_data=f"order_change_status_select:{order.id}"
            )
        for order in orders
    ]
    keyboard.add(*buttons)
    return keyboard