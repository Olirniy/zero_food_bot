import telebot
from config import TG_API_KEY
from log_funcs import logger
# from storage.db import init_db
import time
from storage.db import engine, init_db
from sqlalchemy import inspect

def check_tables():
    init_db()
    inspector = inspect(engine)
    print("Таблицы в БД:", inspector.get_table_names())

check_tables()


def main():
    try:
        # Инициализация БД (без пересоздания таблиц)
        init_db()

        bot = telebot.TeleBot(TG_API_KEY)
        logger.info("Бот запущен")

        @bot.message_handler(commands=['addcategory'])
        def handle_add_category(message):
            try:
                msg = bot.reply_to(message, "📝 Введите название новой категории:")
                bot.register_next_step_handler(msg, process_category_name_step)
            except Exception as e:
                bot.reply_to(message, f"❌ Ошибка: {str(e)}")
                logger.error(f"Error in addcategory handler: {e}")

        def process_category_name_step(message):
            try:
                # Проверяем, что пользователь не отправил команду
                if message.text.startswith('/'):
                    bot.reply_to(message, "⚠️ Пожалуйста, введите название категории, а не команду")
                    return

                category_name = message.text.strip()

                # Проверяем длину названия
                if len(category_name) > 50:  # Ограничение как в вашей модели (VARCHAR(50))
                    bot.reply_to(message, "⚠️ Название слишком длинное (макс. 50 символов)")
                    return

                msg = bot.reply_to(message, "📝 Введите описание категории (или нажмите /skip для пропуска):")
                bot.register_next_step_handler(msg, process_category_desc_step, category_name)
            except Exception as e:
                bot.reply_to(message, f"❌ Ошибка: {str(e)}")
                logger.error(f"Error in process_category_name_step: {e}")

        def process_category_desc_step(message, category_name):
            try:
                from storage.category_storage import add_category  # Импортируем именно так, как у вас

                # Обрабатываем пропуск описания
                if message.text == '/skip':
                    category_description = None
                else:
                    category_description = message.text.strip()
                    if len(category_description) > 255:  # Ограничение как в вашей модели (VARCHAR(255))
                        bot.reply_to(message, "⚠️ Описание слишком длинное (макс. 255 символов)")
                        return

                # Пробуем добавить категорию
                add_category(category_name, category_description)
                bot.reply_to(message, f"✅ Категория '{category_name}' успешно добавлена!")

            except ValueError as e:
                bot.reply_to(message, f"❌ {str(e)}")
            except Exception as e:
                bot.reply_to(message, "❌ Произошла ошибка при добавлении категории")
                logger.error(f"Error adding category: {e}")



        @bot.message_handler(commands=['categories'])
        def handle_list_categories(message):
            from storage.category_storage import get_categories
            categories = get_categories()
            if categories:
                response = "\n".join([f"{c.id}. {c.name}" for c in categories])
            else:
                response = "Категорий пока нет"
            bot.reply_to(message, f"Категории:\n{response}")

        @bot.message_handler(commands=['adddish'])
        def handle_add_dish(message):
            try:
                # Сначала запрашиваем категорию
                msg = bot.reply_to(message, "📝 Введите ID категории для нового блюда:")
                bot.register_next_step_handler(msg, process_dish_category_step)
            except Exception as e:
                bot.reply_to(message, f"❌ Ошибка: {str(e)}")
                logger.error(f"Error in adddish handler: {e}")

        def process_dish_category_step(message):
            try:
                if message.text.startswith('/'):
                    bot.reply_to(message, "⚠️ Пожалуйста, введите ID категории, а не команду")
                    return

                try:
                    category_id = int(message.text.strip())
                except ValueError:
                    bot.reply_to(message, "⚠️ ID категории должен быть числом")
                    return

                msg = bot.reply_to(message, "📝 Введите название блюда:")
                bot.register_next_step_handler(msg, process_dish_name_step, category_id)
            except Exception as e:
                bot.reply_to(message, f"❌ Ошибка: {str(e)}")
                logger.error(f"Error in process_dish_category_step: {e}")

        def process_dish_name_step(message, category_id):
            try:
                if message.text.startswith('/'):
                    bot.reply_to(message, "⚠️ Пожалуйста, введите название блюда, а не команду")
                    return

                dish_name = message.text.strip()
                if len(dish_name) > 100:  # Ограничение как в вашей модели (VARCHAR(100))
                    bot.reply_to(message, "⚠️ Название слишком длинное (макс. 100 символов)")
                    return

                msg = bot.reply_to(message, "📝 Введите описание блюда (или /skip для пропуска):")
                bot.register_next_step_handler(msg, process_dish_desc_step, category_id, dish_name)
            except Exception as e:
                bot.reply_to(message, f"❌ Ошибка: {str(e)}")
                logger.error(f"Error in process_dish_name_step: {e}")

        def process_dish_desc_step(message, category_id, dish_name):
            try:
                if message.text == '/skip':
                    dish_description = None
                else:
                    if message.text.startswith('/'):
                        bot.reply_to(message, "⚠️ Пожалуйста, введите описание блюда, а не команду")
                        return

                    dish_description = message.text.strip()
                    if len(dish_description) > 255:  # Ограничение как в вашей модели (VARCHAR(255))
                        bot.reply_to(message, "⚠️ Описание слишком длинное (макс. 255 символов)")
                        return

                msg = bot.reply_to(message, "📝 Введите цену блюда (только число, например 250.50):")
                bot.register_next_step_handler(msg, process_dish_price_step, category_id, dish_name, dish_description)
            except Exception as e:
                bot.reply_to(message, f"❌ Ошибка: {str(e)}")
                logger.error(f"Error in process_dish_desc_step: {e}")

        def process_dish_price_step(message, category_id, dish_name, dish_description):
            try:
                if message.text.startswith('/'):
                    bot.reply_to(message, "⚠️ Пожалуйста, введите цену, а не команду")
                    return

                try:
                    price = float(message.text.strip())
                    if price <= 0:
                        bot.reply_to(message, "⚠️ Цена должна быть больше нуля")
                        return
                except ValueError:
                    bot.reply_to(message, "⚠️ Цена должна быть числом (например: 250 или 199.99)")
                    return

                msg = bot.reply_to(message, "📝 Введите URL изображения (или /skip для пропуска):")
                bot.register_next_step_handler(msg, process_dish_image_step, category_id, dish_name, dish_description,
                                               price)
            except Exception as e:
                bot.reply_to(message, f"❌ Ошибка: {str(e)}")
                logger.error(f"Error in process_dish_price_step: {e}")

        def process_dish_image_step(message, category_id, dish_name, dish_description, price):
            try:
                from storage.dish_storage import add_dish  # Импортируем как в вашем исходном коде

                if message.text == '/skip':
                    image_url = None
                else:
                    if message.text.startswith('/'):
                        bot.reply_to(message, "⚠️ Пожалуйста, введите URL, а не команду")
                        return

                    image_url = message.text.strip()
                    if len(image_url) > 255:  # Ограничение как в вашей модели (VARCHAR(255))
                        bot.reply_to(message, "⚠️ URL слишком длинный (макс. 255 символов)")
                        return

                # Добавляем блюдо
                add_dish(
                    category_id=category_id,
                    name=dish_name,
                    description=dish_description,
                    price=price,
                    image_url=image_url
                )
                bot.reply_to(message, f"✅ Блюдо '{dish_name}' успешно добавлено!")

            except ValueError as e:
                bot.reply_to(message, f"❌ {str(e)}")
            except Exception as e:
                bot.reply_to(message, "❌ Произошла ошибка при добавлении блюда")
                logger.error(f"Error adding dish: {e}")

        @bot.message_handler(commands=['dishes'])
        def handle_list_dishes(message):
            from storage.dish_storage import get_all_dishes_by_category
            dishes = get_all_dishes_by_category(1)  # Получаем блюда из категории с ID=1
            if dishes:
                response = "\n".join([f"{d.id}. {d.name} — {d.price} руб." for d in dishes])
            else:
                response = "Блюд пока нет"
            bot.reply_to(message, f"Блюда:\n{response}")


        @bot.message_handler(commands=['start'])
        def handle_start(message):
            from models.user import User
            from storage.user_storage import add_user

            try:
                user = User(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name
                )
                add_user(user)
                bot.reply_to(message, "✅ Регистрация успешна!")
            except Exception as e:
                logger.error(f"Ошибка регистрации: {e}")
                bot.reply_to(message, "❌ Ошибка регистрации")

        # Запуск бота
        bot.infinity_polling(long_polling_timeout=10)

    except Exception as e:
        logger.critical(f"Фатальная ошибка: {e}")
        raise

if __name__ == "__main__":
    main()
    try:
        # Удерживаем выполнение, чтобы бот работал
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Бот остановлен.")

