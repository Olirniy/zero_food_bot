from typing import Optional, Union
from unittest.mock import call

from telebot import types
from telebot import TeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from models import dish
from repository.user_repo import UserRepository
from repository.dish_repo import DishRepository
from repository.order_repo import OrderRepository
from repository.order_item_repo import OrderItemRepository
from storage.user_storage import UserStorage
from storage.dish_storage import DishStorage
from storage.order_storage import OrderStorage
from storage.order_items_storage import OrderItemStorage
from models.enums import OrderStatus
from models.order import Order  # Важно добавить!
from models.dish import Dish
from utils.logger import setup_logger  # Добавить в импорты
logger = setup_logger(__name__)  # После всех импортов
logger.debug(f"Импортирован {__name__}")



def register_cart_handlers(bot: TeleBot, db, sql_data: dict):
    # Инициализация storage
    user_storage = UserStorage(db, sql_data)
    dish_storage = DishStorage(db, sql_data)
    order_storage = OrderStorage(db, sql_data)
    order_item_storage = OrderItemStorage(db, sql_data)

    # Инициализация репозиториев
    user_repo = UserRepository(user_storage)
    dish_repo = DishRepository(dish_storage)
    order_repo = OrderRepository(order_storage, OrderItemRepository(order_item_storage))
    order_item_repo = OrderItemRepository(order_item_storage)

    def get_current_cart_state(chat_id, message_id):
        """Возвращает текущий текст и разметку сообщения с корзиной"""
        try:
            # Получаем текущее сообщение
            msg = bot.get_message(chat_id, message_id)
            return (msg.text, str(msg.reply_markup))
        except Exception as e:
            logger.error(f"Ошибка получения состояния корзины: {e}")
            return (None, None)


    def get_in_cart(self, user_id: int) -> Optional['Order']:
        try:
            """Находит корзину пользователя (IN_CART)"""
            orders = self.get_all_by_user(user_id)
            for order in orders:
                if order.status == OrderStatus.IN_CART:
                    return order
            # Если корзина не найдена - создаем новую
            return self.create(user_id, OrderStatus.IN_CART)
        except Exception as e:
            logger.error(f"Ошибка получения корзины: {e}", exc_info=True)
            return None

    # Проверка наличия класса Order
    try:
        from models.order import Order
        logger.debug(f"Order class: {Order}")
    except ImportError as e:
        logger.critical(f"Ошибка импорта Order: {e}", exc_info=True)
        raise


    # Функция для добавления блюда в корзину
    @bot.callback_query_handler(func=lambda call: call.data.startswith('add_'))
    def add_to_cart(call: CallbackQuery):
        try:
            user = user_repo.get_or_create(
                telegram_id=call.from_user.id,
                username=call.from_user.username or f"user_{call.from_user.id}"
            )

            dish_id = int(call.data.split('_')[1])
            dish = dish_repo.get_by_id(dish_id)

            if not dish:
                bot.answer_callback_query(call.id, "❌ Блюдо не найдено")
                return

            # Получаем или создаем корзину (теперь гарантированно получим объект)
            cart = order_repo.get_in_cart(user.id)

            # Добавляем товар
            order_item_repo.add_item(cart.id, dish, 1)
            bot.answer_callback_query(call.id, f"✅ {dish.name} добавлен в корзину")

        except Exception as e:
            logger.error(f"Ошибка добавления: {e}", exc_info=True)
            bot.answer_callback_query(call.id, "❌ Ошибка при добавлении")




    @bot.message_handler(commands=['cart'])
    # Функция для отображения корзины пользователя
    def show_cart(message: Union[Message, CallbackQuery], edit_message_id=None, dish_name=None, new_quantity=None,
                  check_only=None, response=None, markup=None):
        try:
            if isinstance(message, CallbackQuery):
                chat_id = message.message.chat.id
                user_id = message.from_user.id
                message_obj = message.message
            else:
                chat_id = message.chat.id
                user_id = message.from_user.id
                message_obj = message

            logger.info(f"Загрузка корзины для пользователя {user_id}")

            user = user_repo.get_or_create(
                telegram_id=user_id,
                username=message_obj.from_user.username or f"user_{user_id}"
            )
            logger.debug(f"Пользователь: {user.id}")

            cart = order_repo.get_in_cart(user.id)
            logger.debug(f"Корзина: {cart.id if cart else 'не найдена'}")




            if not cart:
                cart = order_repo.create(user.id, OrderStatus.IN_CART)
                logger.info(f"Создана новая корзина: {cart.id}")

            items = order_item_repo.get_by_order(cart.id)
            logger.debug(f"Найдено позиций: {len(items)}")



            # Формирование сообщения
            response = "🛒 *Ваша корзина:*\n\n"
            total = 0
            grouped_items = {}

            for item in items:
                logger.debug(f"Обработка позиции: {item.id} - {item.dish.name}")

                if item.dish.name not in grouped_items:
                    grouped_items[item.dish.name] = {
                        'dish': item.dish,
                        'quantity': 0,
                        'items': []
                    }
                grouped_items[item.dish.name]['quantity'] += item.quantity
                grouped_items[item.dish.name]['items'].append(item)
                total += item.dish.price * item.quantity

            # Добавление товаров в сообщение
            for name, data in grouped_items.items():
                response += f"🍽 *{name}*\n"
                response += f"   Количество: {data['quantity']} x {data['dish'].price}₽ = {data['quantity'] * data['dish'].price}₽\n\n"

            response += f"*Итого: {total}₽*"
            logger.debug(f"Сформирован текст корзины:\n{response}")

            # Создание клавиатуры
            markup = InlineKeyboardMarkup(row_width=3)
            for name, data in grouped_items.items():
                markup.add(
                    InlineKeyboardButton(f"➕ {name}", callback_data=f"inc_{data['items'][0].id}"),
                    InlineKeyboardButton(f"➖ {name}", callback_data=f"dec_{data['items'][0].id}"),
                    InlineKeyboardButton(f"❌ {name}", callback_data=f"remove_{data['items'][0].id}")
                )

            markup.row(
                InlineKeyboardButton("🔄 Обновить", callback_data="refresh_cart"),
                InlineKeyboardButton("✅ Оформить", callback_data="checkout")
            )

            # Проверка, нужно ли только проверить состояние (без обновления)
            if check_only:
                current_state = get_current_cart_state(chat_id, edit_message_id)
                new_state = (response, str(markup))
                return current_state != new_state


            # Обработка отправки/обновления сообщения
            try:
                if edit_message_id:
                    # ... [код обновления сообщения] ...
                    # Изменяем только если есть изменения
                    if edit_message_id:
                        # Всегда пытаемся обновить сообщение
                        bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=edit_message_id,
                            text=response,
                            parse_mode="Markdown",
                            reply_markup=markup
                        )
                        logger.debug("Корзина обновлена")
                    else:
                        logger.debug("Корзина не изменилась")
                else:
                    bot.send_message(
                        chat_id,
                        response,
                        parse_mode="Markdown",
                        reply_markup=markup
                    )
                    logger.debug("Новая корзина отправлена")
                # После bot.edit_message_text
                if isinstance(message, CallbackQuery):
                    try:
                        bot.answer_callback_query(
                            message.id,
                            f"Количество изменено: {dish_name} - {new_quantity}",
                            show_alert=False
                        )
                    except Exception:
                        logger.debug("Callback уже обработан")
            except Exception as e:
                if "message is not modified" in str(e):
                    logger.debug("Корзина уже актуальна")
                    # Можно добавить легкое уведомление
                    if isinstance(message, CallbackQuery):
                        bot.answer_callback_query(
                            message.id,
                            "🔄 Корзина не изменилась",
                            show_alert=False
                        )
                else:
                    logger.error(f"Ошибка Telegram API: {e}")
                    raise


        # ... [существующий код] ...
        except Exception as e:
            if "message is not modified" in str(e):
                logger.debug("Корзина уже актуальна")
                # Удаляем эту часть, чтобы избежать двойного ответа
            else:
                logger.error(f"Ошибка Telegram API: {e}")
                raise

        except Exception as e:
            logger.error(f"Критическая ошибка в корзине: {e}", exc_info=True)
            if isinstance(message, CallbackQuery):
                bot.answer_callback_query(
                    message.id,
                    "❌ Ошибка при загрузке корзины",
                    show_alert=True
                )
            else:
                bot.reply_to(message, "❌ Ошибка при загрузке корзины")





    @bot.callback_query_handler(func=lambda call: call.data.startswith(('inc_', 'dec_', 'remove_')))
    def handle_cart_actions(call: CallbackQuery):
        try:
            bot.answer_callback_query(call.id)
            action, item_id = call.data.split('_', 1)
            item_id = int(item_id)
            logger.info(f"Обработка действия: {action} для позиции {item_id}")

            item = order_item_repo.get_by_id(item_id)
            if not item:
                logger.error(f"Позиция {item_id} не найдена")
                bot.answer_callback_query(call.id, "❌ Позиция не найдена")
                return

            if action == 'inc':
                order_item_repo.update_quantity(item_id, item.quantity + 1)
                logger.debug(f"Увеличено количество: {item_id} -> {item.quantity + 1}")
            elif action == 'dec':
                if item.quantity > 1:
                    order_item_repo.update_quantity(item_id, item.quantity - 1)
                    logger.debug(f"Уменьшено количество: {item_id} -> {item.quantity - 1}")
                else:
                    order_item_repo.delete_item(item_id)
                    logger.debug(f"Удалена позиция: {item_id}")
            elif action == 'remove':
                order_item_repo.delete_item(item_id)
                logger.debug(f"Удалена позиция: {item_id}")

            # Добавляем уведомление о действии
            action_names = {
                'inc': "увеличено",
                'dec': "уменьшено",
                'remove': "удалено"
            }
            bot.answer_callback_query(
                call.id,
                f"✅ {item.dish.name} {action_names[action]}",
                show_alert=False
            )

            # Обновляем корзину
            show_cart(call, edit_message_id=call.message.message_id)

        except Exception as e:
            logger.error(f"Ошибка обработки действия: {e}", exc_info=True)
            bot.answer_callback_query(
                call.id,
                "❌ Ошибка при обновлении",
                show_alert=True
            )


    @bot.callback_query_handler(func=lambda call: call.data == "refresh_cart")
    def refresh_cart(call: CallbackQuery):
        try:
            # Проверяем, изменилась ли корзина
            cart_changed = show_cart(call, edit_message_id=call.message.message_id, check_only=True)

            if not cart_changed:
                # Отправляем уведомление, что корзина актуальна
                bot.answer_callback_query(
                    call.id,
                    "🔄 Корзина уже актуальна!",
                    show_alert=False
                )
            else:
                bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"Ошибка обновления корзины: {e}")
            bot.answer_callback_query(
                call.id,
                "❌ Ошибка при обновлении",
                show_alert=False
            )


    def cart_changed(message_id: int, new_text: str, new_markup: InlineKeyboardMarkup) -> bool:
        """Проверяет, изменилась ли корзина"""
    # Здесь можно добавить логику сравнения с предыдущим состоянием
    # Пока будем всегда возвращать True для простоты
    return True




    @bot.callback_query_handler(func=lambda call: call.data == 'checkout')
    # Логика оформления заказа
    def checkout(call: CallbackQuery):
        bot.answer_callback_query(call.id, "Переход к оформлению заказа")
        # Здесь будет логика оформления заказа