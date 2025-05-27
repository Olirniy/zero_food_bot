import os

from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


from app.bot import ZeroFoodBot
from builders.main_menu_builder import MainMenuBuilder
from keyboards.inline_keyboards import get_dish_keyboard, get_continue_checkout, get_dish_keyboard_with_add, select_payment_method_keyboard, select_order_to_change_status
from config import DEFAULT_IMG_PATH
from models.enums import OrderStatus, PaymentMethod

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
        orders = bot.get_order_repository().get_all_by_user(message.chat.id)
        bot.send_message(message.chat.id, "Ваши заказы:")
        for order in orders:
            if order.status == OrderStatus.IN_CART:
                continue
            bot.send_message(message.chat.id, order.get_order_text())

    # отображение корзины
    def show_cart(message: types.Message) -> None:
        print("show_cart")
        user_id = message.chat.id

        # Получаем текущий заказ со статусом "IN_CART"
        order = bot.get_order_repository().get_in_cart(user_id)

        if not order or not order.items:
            # Если нет заказа или он пустой
            bot.send_message(user_id, "🧺 Ваша корзина пуста.")
            return

        # Формируем сообщение со списком блюд
        total = 0
        text = "🛒 <b>Ваша корзина:</b>\n\n"
        for item in order.items:
            subtotal = item.quantity * item.dish_price
            total += subtotal
            text += f"🍽 {item.dish_name} x{item.quantity} — {subtotal}₽\n"
        text += f"\n💰 <b>Итого:</b> {total}₽"

        # Добавляем кнопку "Оформить заказ"
        markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton("✅ Оформить заказ", callback_data="confirm_order")
        )
        bot.send_message(user_id, text, parse_mode='HTML', reply_markup=markup)

    # Запрос отзыва
    def leave_review(message: types.Message) -> None:
        print("leave_review")
        user_id = message.chat.id
        user_states[user_id] = "awaiting_review"
        bot.send_message(message.chat.id, "Пожалуйста, напишите ваш отзыв:")
        return

    # Функция админа - вывод всех отзывов
    def admin_reviews(message: types.Message) -> None:
        print(f"admin_reviews {message.from_user.id} {message.from_user.username}")
        from config import ADMINS

        user_id = message.chat.id

        if user_id not in ADMINS:
            bot.send_message(message.chat.id, "У вас нет доступа к этой команде.")
            return

        reviews = bot.get_feedback_repository().get_all()

        if not reviews:
            bot.send_message(message.chat.id, "Отзывов пока нет.")
            return

        message_text = "📋 Все отзывы:\n\n"
        for review in reviews:
            message_text += f"📅 {review.created_at.strftime('%d.%m.%Y %H:%M')}\n"
            message_text += f"👤 @{review.user_name}\n"
            message_text += f"📝 Отзыв: {review.text}\n"
            message_text += "-" * 30 + "\n"

        # Разбиваем на части, если слишком длинное
        max_length = 4096
        for i in range(0, len(message_text), max_length):
            chunk = message_text[i:i + max_length]
            bot.send_message(message.chat.id, chunk)

    def clear_cart(message: types.Message) -> None:
        print("clear_cart")
        order = bot.get_order_repository().get_in_cart(message.chat.id)
        if not order:
            bot.send_message(message.chat.id, "🧺 Ваша корзина пуста.")
            return

        if not order.items:
            bot.send_message(message.chat.id, "🧺 Ваша корзина пуста.")
            return

        items = bot.get_order_item_repository().get_by_order(order.id)

        for i in items:
            print(f"deleting {i.id} {i.dish_name}")
            bot.get_order_item_repository().delete_item(i.id)
            order.del_item(i)
        bot.get_order_repository().save(order)
        bot.send_message(message.chat.id, "🧺 Корзина очищена.")

    #отображение главного меню
    @bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("cmd_"))
    def process_command(callback_query: types.CallbackQuery) -> None:
        print("process_command")
        command: str = callback_query.data.split(":", 1)[1]
        if command == "show_menu":
            show_categories(callback_query.message)
        elif command == "show_cart":
            show_cart(callback_query.message)
        elif command == "clear_cart":
            clear_cart(callback_query.message)
        elif command == "show_orders":
            show_orders(callback_query.message)
        elif command == "add_feedback":
            leave_review(callback_query.message)
        elif command == "show_feedbacks":
            admin_reviews(callback_query.message)
        elif command == "load_menu":
            msg: types.Message = bot.send_message(
                callback_query.message.chat.id,
                "Пожалуйста, отправьте файл с новым меню:"
            )
            bot.register_next_step_handler(msg, handle_menu_file)
        elif command == "change_order_status":
            orders = bot.get_order_repository().get_orders_by_status(OrderStatus.PENDING)
            orders.extend(bot.get_order_repository().get_orders_by_status(OrderStatus.PREPARING))
            msg: types.Message = bot.send_message(
                callback_query.message.chat.id,
                "Выберите заказ, которому нужно присвоить следующий статус:",
                reply_markup=select_order_to_change_status(orders)
            )

    @bot.message_handler(commands=['start'])
    def cmd_start(message: types.Message) -> None:
        markup = MainMenuBuilder.build_menu(message.from_user.id)
        bot.send_message(chat_id=message.chat.id, text="Выберите действие:", reply_markup=markup)

    @bot.message_handler(commands=['help'])
    def cmd_help(message: types.Message) -> None:
        bot.send_message(chat_id=message.chat.id, text="Нажмите start, добавьте блюда в корзину и оформите заказ")

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
        print(f"show_dishes_by_category {category_id}")
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
                        reply_markup=get_dish_keyboard_with_add(dish.id)
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
            # получаем существующий caption (подпись к фото)
            existing_caption: str = call.message.caption or ""
            # формируем новый caption, дописывая описание к старому
            new_caption: str = f"{existing_caption}\n\n<b>Подробное описание:</b>\n{dish.description}"

            bot.edit_message_caption(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                caption=new_caption,
                parse_mode='HTML',
                reply_markup=get_dish_keyboard(dish.id)
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
        except ValueError:
            bot.send_message(message.chat.id, "Введите число!")
            bot.register_next_step_handler(message, lambda m: ask_quantity(m, dish))
            return

        order = bot.get_order_repository().get_in_cart(message.from_user.id)
        if not order:
            order = bot.get_order_repository().create(message.from_user.id)

        order_item = order.get_item_by_dish_id(dish.id)
        if not order_item:
            order_item = bot.get_order_item_repository().new_item(order_id=order.id, dish_id=dish.id, dish_name=dish.name, dish_price=dish.price, quantity= quantity)
        else:
            order_item.quantity += quantity
            bot.get_order_item_repository().update_quantity(order_item.id, order_item.quantity)
        order.update_item(order_item)
        bot.get_order_repository().save(order)
        text=f"Добавлено в корзину:\n{dish.name} x{quantity}\n Ваша корзина состоит из:\n"+order.get_order_text()
        bot.send_message(
            message.chat.id,
                text,
            reply_markup=get_continue_checkout()
        )


    @bot.callback_query_handler(func=lambda call: call.data == 'continue_shopping')
    def continue_shopping(call):
        show_categories(call.message)

    # Получение отзыва, обработка отзыва и запись отзыва в базу отзывов
    @bot.message_handler(content_types=['text'])
    def handle_message(message: types.Message) -> None:
        print("handle_message")
        user_id = message.chat.id
        user_name = message.chat.username
        text = message.text

        if user_states.get(user_id) == "awaiting_review":
            bot.get_feedback_repository().new_feedback(user_id, user_name, text)
            bot.send_message(message.chat.id, "Спасибо за ваш отзыв!")
            user_states[user_id] = None
        else:
            bot.send_message(message.chat.id, "Я не ожидал сообщение от вас. Используйте команды.")

    @bot.callback_query_handler(func=lambda call: call.data == 'confirm_order')
    def confirm_order(call: types.CallbackQuery) -> None:
        print("confirm_order")
        user_id = call.from_user.id

        # Снова получаем заказ — на случай, если он изменился
        order = bot.get_order_repository().get_in_cart(user_id)

        if not order:
            # Если заказа нет — сообщаем
            bot.answer_callback_query(call.id, text="Корзина пуста.")
            return

        # Сообщаем пользователю, что он может выбрать способ оплаты
        bot.send_message(
            chat_id=call.message.chat.id,
            text=f"Выберите способ оплаты для заказа номер {order.id}:",
            reply_markup=select_payment_method_keyboard(order.id)
        )

    @bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("order_change_status_select:"))
    def change_order_status(callback_query: types.CallbackQuery) -> None:
        order_id: int = int(callback_query.data.split(":", 1)[1])
        order = bot.get_order_repository().get_by_id(order_id)
        if order:
            if order.status == OrderStatus.PENDING:
                order.status = OrderStatus.PREPARING
            elif order.status == OrderStatus.PREPARING:
                order.status = OrderStatus.DONE
            bot.get_order_repository().save(order)
            bot.send_message(order.user_id, text=f"Статус вашего заказа {order.id} изменен на {order.status.get_name()}")

        response_text: str = f"Статус заказа изменен на {order.status.get_name()}"
        bot.send_message(chat_id=callback_query.message.chat.id, text=response_text)


    @bot.callback_query_handler(func=lambda call: call.data.startswith('select_payment_'))
    def select_payment_method(call):
        print("add_to_cart")
        data = call.data.split('_')[2]
        method = data.split(':')[0]
        order_id = int(data.split(':')[1])
        order = bot.get_order_repository().get_by_id(order_id)
        if not order:
            bot.answer_callback_query(call.id, text="Заказ не найден.")
            return
        if method == "cash":
            order.payment_method = PaymentMethod.CASH
        elif method == "card":
            order.payment_method = PaymentMethod.ONLINE
        # Меняем статус заказа на "PENDING"
        order.status = OrderStatus.PENDING
        bot.get_order_repository().save(order)

        # Сообщаем пользователю об успешном оформлении
        bot.send_message(
            chat_id=call.message.chat.id,
            text=f"✅ Ваш заказ номер {order.id} успешно оформлен! В ближайшее время вам напишет оператор для подтверждения"
        )

        text = f"🆕 Новый заказ от пользователя {order.user_id}.\n" + order.get_order_text()
        # Уведомляем админов о новом заказе
        from config import ADMIN_GROUP_ID
        bot.send_message(
            ADMIN_GROUP_ID,
            text
        )

    def handle_menu_file(message: types.Message) -> None:
        # Проверяем, что пользователь прислал документ
        if not message.document:
            bot.send_message(message.chat.id, "Это не файл. Пожалуйста, отправьте документ.")
            bot.register_next_step_handler(message, handle_menu_file)
            return

        # Скачиваем файл
        file_info = bot.get_file(message.document.file_id)
        file_bytes: bytes = bot.download_file(file_info.file_path)

        # Сохраняем локально
        import os
        os.makedirs("new_menus", exist_ok=True)
        file_path: str = os.path.join("new_menus", message.document.file_name)
        with open(file_path, 'wb') as f:
            f.write(file_bytes)

        # Загружаем меню через menu_loader
        try:
            bot.menu_loader.load_menu(file_path)
            bot.send_message(message.chat.id, "✅ Новое меню успешно загружено.")
        except Exception as e:
            bot.send_message(message.chat.id, f"❗ Ошибка при загрузке меню: {e}")