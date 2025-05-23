import os

from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


from app.bot import ZeroFoodBot
from builders.main_menu_builder import MainMenuBuilder
from keyboards.inline_keyboards import get_dish_keyboard, get_continue_checkout
from config import DEFAULT_IMG_PATH
# Храним временные состояния пользователей
user_states = {}

def init_handlers(bot: ZeroFoodBot) -> None:
    def show_categories(message: types.Message) -> None:
        print("show_categories")
        if not bot.category_menu_builder:
            bot.send_message(chat_id=message.chat.id, text="Категории не загружены")
            return
        markup: InlineKeyboardMarkup = bot.category_menu_builder.build_menu()
        bot.send_message(chat_id=message.chat.id, text="Пожалуйста, выберите категорию:", reply_markup=markup)

    # отображение заказов
    def show_orders(message: types.Message) -> None:
        bot.send_message(message.chat.id, "Ваши заказы будут здесь")

    # отображение корзины
    def show_cart(message: types.Message) -> None:
        bot.send_message(message.chat.id, "Ваша корзина будет здесь")

    # Запрос отзыва
    def leave_review(message: types.Message) -> None:
        print("leave_review")
        user_id = message.from_user.id
        user_states[user_id] = "awaiting_review"
        bot.send_message(message.chat.id, "Пожалуйста, напишите ваш отзыв:")
        return

    # Функция админа - вывод всех отзывов
    def admin_reviews(message: types.Message) -> None:
        print("admin_reviews")
        from config import ADMINS

        user_id = message.from_user.id

        if user_id not in ADMINS:
            bot.send_message(message.chat.id, "У вас нет доступа к этой команде.")
            return

        reviews = bot.get_feedback_repository().get_all()

        if not reviews:
            bot.send_message(message.chat.id, "Отзывов пока нет.")
            return

        message_text = "📋 Все отзывы:\n\n"
        for review in reviews:
            _, user_id, username, text, created_at = review
            message_text += f"📅 {created_at}\n"
            message_text += f"👤 ID: {user_id}, @{username}\n"
            message_text += f"📝 Отзыв: {text}\n"
            message_text += "-" * 30 + "\n"

        # Разбиваем на части, если слишком длинное
        max_length = 4096
        for i in range(0, len(message_text), max_length):
            chunk = message_text[i:i + max_length]
            bot.send_message(message.chat.id, chunk)


    #отображение главного меню
    @bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("cmd_"))
    def process_command(callback_query: types.CallbackQuery) -> None:
        print("process_command")
        command: str = callback_query.data.split(":", 1)[1]
        if command == "show_menu":
            show_categories(callback_query.message)
        elif command == "show_cart":
            show_cart(callback_query.message)
        elif command == "show_orders":
            show_orders(callback_query.message)
        elif command == "add_feedback":
            leave_review(callback_query.message)
        elif command == "show_feedbacks":
            admin_reviews(callback_query.message)
        elif command == "load_menu":
            pass
        elif command == "change_order_status":
            pass

    @bot.message_handler(commands=['start'])
    def cmd_start(message: types.Message) -> None:
        markup = MainMenuBuilder.build_menu(message.from_user.id)
        bot.send_message(chat_id=message.chat.id, text="Выберите действие:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("category_select:"))
    def process_category(callback_query: types.CallbackQuery) -> None:
        print("process_category")
        category_id: int = int(callback_query.data.split(":", 1)[1])
        category = bot.get_category_repository().get_by_id(category_id)
        if category:
            show_dishes_by_category(callback_query, category.id)
        else:
            response_text: str = "Категория не найдена"
            bot.answer_callback_query(callback_query_id=callback_query.id, text=response_text)

    def show_dishes_by_category(call, category_id):
        print("show_dishes_by_category")
        dishes = bot.get_dish_repository().get_by_category(category_id)

        if not dishes:
            bot.send_message(call.message.chat.id, "Блюда не найдены.")
            return

        for dish in dishes:
            # Определяем, какой путь к фото использовать
            if dish.photo_url and os.path.exists(dish.photo_url):
                photo_path = dish.photo_url
            else:
                photo_path = DEFAULT_IMG_PATH

            try:
                with open(photo_path, 'rb') as photo:
                    bot.send_photo(
                        chat_id=call.message.chat.id,
                        photo=photo,
                        caption=(
                            f"<b>{dish.name}</b>\n"
                            f"{dish.short_description}\n\n"
                            f"Цена: {dish.price} ₽"
                        ),
                        parse_mode='HTML',
                        reply_markup=get_dish_keyboard(dish.id)
                    )
            except Exception as e:
                bot.send_message(
                    call.message.chat.id,
                    f"Ошибка при отображении {dish.name}: {e}"
                )

    @bot.callback_query_handler(func=lambda call: call.data.startswith('details_'))
    def show_dish_details(call):
        print("show_dish_details")
        dish_id = int(call.data.split('_')[1])
        dish = bot.get_dish_repository().get_by_id(dish_id)
        if dish:
            bot.send_message(
                call.message.chat.id,
                f"<b>Подробное описание:</b>\n{dish.description}",
                parse_mode='HTML'
            )

    @bot.callback_query_handler(func=lambda call: call.data.startswith('add_'))
    def add_to_cart(call):
        print("add_to_cart")
        dish_id = int(call.data.split('_')[1])
        dish = bot.get_dish_repository().get_by_id(dish_id)

        msg = bot.send_message(
            call.message.chat.id,
            f"Введите количество для '{dish.name}':"
        )
        bot.register_next_step_handler(msg, lambda m: ask_quantity(m, dish))

    def ask_quantity(message, dish):
        print("ask_quantity")
        try:
            quantity = int(message.text)
            total_price = dish.price * quantity
            order = bot.get_order_repository().get_in_cart(message.from_user.id)
            if not order:
                order = bot.get_order_repository().create(message.from_user.id)

            order_item = order.get_item_by_dish_id(dish.id)
            if not order_item:
                order_item = bot.get_order_item_repository().create(order.id, dish.id, quantity)
            else:
                order_item.quantity += quantity
            order.update_item(order_item)
            bot.get_order_repository().save(order)
            bot.send_message(
                message.chat.id,
                f"Добавлено в корзину:\n{dish.name} x{quantity}\nИтого: {total_price} ₽",
                reply_markup=get_continue_checkout()
            )
        except ValueError:
            bot.send_message(message.chat.id, "Введите число!")
            bot.register_next_step_handler(message, lambda m: ask_quantity(m, dish))

    @bot.callback_query_handler(func=lambda call: call.data == 'continue_shopping')
    def continue_shopping(call):
        print("continue_shopping")
        show_categories(call.message)

    @bot.callback_query_handler(func=lambda call: call.data == 'checkout')
    def checkout_order(call):
        print("checkout_order")
        bot.send_message(call.message.chat.id, "Ваш заказ оформлен! Ожидайте.")

    # Получение отзыва, обработка отзыва и запись отзыва в базу отзывов
    @bot.message_handler(content_types=['text'])
    def handle_message(message: types.Message) -> None:
        print("handle_message")
        user_id = message.from_user.id
        text = message.text

        if user_states.get(user_id) == "awaiting_review":
            bot.get_feedback_repository().new_feedback(user_id, text)
            bot.send_message(message.chat.id, "Спасибо за ваш отзыв!")
            user_states[user_id] = None
        else:
            bot.send_message(message.chat.id, "Я не ожидал сообщение от вас. Используйте команды.")