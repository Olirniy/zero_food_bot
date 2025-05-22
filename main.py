import telebot
from config import TG_API_KEY
from log_funcs import logger
from storage.db import init_db
import time
from storage.db import engine, init_db
from sqlalchemy import inspect
from telebot import types
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class DishHandler:
    def __init__(self, bot):
        self.bot = bot

    def log_input(self, step: str, user_input: str, user_id: int):
        """Логирование ввода пользователя"""
        logger.info(f"User {user_id} at step '{step}': {user_input}")

    def process_dish_image(self, message, category_id, dish_name, description, price):
        try:
            from storage.dish_storage import add_dish

            self.log_input("image_url", message.text, message.from_user.id)
            image_url = None if message.text == '/skip' else message.text.strip()

            if image_url:
                parsed = urlparse(image_url)
                if not all([parsed.scheme, parsed.netloc]):
                    raise ValueError("URL должен начинаться с http:// или https://")
                if len(image_url) > 255:
                    raise ValueError("URL слишком длинный (макс. 255 символов)")

            add_dish(
                name=str(dish_name),
                description=str(description) if description else None,
                price=float(price),
                category_id=int(category_id),
                image_url=str(image_url) if image_url else None
            )
            self.bot.reply_to(message, f"✅ Блюдо '{dish_name}' успешно добавлено!")

        except ValueError as e:
            self.bot.reply_to(message, f"❌ {str(e)}")
            logger.error(f"Image URL error from user {message.from_user.id}: {e}")
        except Exception as e:
            self.bot.reply_to(message, "❌ Произошла ошибка при добавлении блюда")
            logger.error(f"Dish addition error from user {message.from_user.id}: {e}")

    def process_dish_price(self, message, category_id, dish_name, description):
        try:
            self.log_input("price", message.text, message.from_user.id)
            price = message.text.strip().replace(',', '.')

            if not price.replace('.', '').isdigit():
                raise ValueError("Цена должна быть числом (например: 250.50)")

            price = float(price)
            if price <= 0:
                raise ValueError("Цена должна быть больше нуля")

            msg = self.bot.reply_to(message, "Введите URL изображения (или /skip):")
            self.bot.register_next_step_handler(msg,
                                                lambda m: self.process_dish_image(m, category_id, dish_name,
                                                                                  description, price))

        except ValueError as e:
            self.bot.reply_to(message, f"❌ {str(e)}")
            logger.warning(f"Invalid price from user {message.from_user.id}: {message.text}")
            msg = self.bot.reply_to(message, "Пожалуйста, введите цену еще раз:")
            self.bot.register_next_step_handler(msg,
                                                lambda m: self.process_dish_price(m, category_id, dish_name,
                                                                                  description))
        except Exception as e:
            self.bot.reply_to(message, "❌ Критическая ошибка")
            logger.error(f"Price processing error from user {message.from_user.id}: {e}")

    def process_dish_description(self, message, category_id, dish_name):
        try:
            self.log_input("description", message.text, message.from_user.id)
            description = None if message.text == '/skip' else message.text.strip()

            if description and len(description) > 255:
                raise ValueError("Описание слишком длинное (макс. 255 символов)")

            msg = self.bot.reply_to(message, "Введите цену блюда (например: 250.50):")
            self.bot.register_next_step_handler(msg,
                                                lambda m: self.process_dish_price(m, category_id, dish_name,
                                                                                  description))

        except ValueError as e:
            self.bot.reply_to(message, f"❌ {str(e)}")
            logger.warning(f"Invalid description from user {message.from_user.id}: {message.text}")
        except Exception as e:
            self.bot.reply_to(message, "❌ Ошибка ввода")
            logger.error(f"Description processing error from user {message.from_user.id}: {e}")

    def process_dish_name(self, message, category_id):
        try:
            self.log_input("dish_name", message.text, message.from_user.id)
            dish_name = message.text.strip()

            if dish_name.isdigit():
                raise ValueError("Название не может быть числом")
            if len(dish_name) > 100:
                raise ValueError("Название слишком длинное (макс. 100 символов)")

            msg = self.bot.reply_to(message, "Введите описание блюда (или /skip):")
            self.bot.register_next_step_handler(msg,
                                                lambda m: self.process_dish_description(m, category_id,
                                                                                        dish_name))

        except ValueError as e:
            self.bot.reply_to(message, f"❌ {str(e)}")
            logger.warning(f"Invalid dish name from user {message.from_user.id}: {message.text}")
            self.handle_add_dish(message)  # Перезапускаем процесс
        except Exception as e:
            self.bot.reply_to(message, "❌ Ошибка ввода")
            logger.error(f"Name processing error from user {message.from_user.id}: {e}")

    def process_category_choice(self, message):
        try:
            self.log_input("category", message.text, message.from_user.id)
            category_id = int(message.text.split('.')[0])
            msg = self.bot.reply_to(message, "Введите название блюда:",
                                    reply_markup=types.ReplyKeyboardRemove())
            self.bot.register_next_step_handler(msg,
                                                lambda m: self.process_dish_name(m, category_id))

        except (IndexError, ValueError):
            self.bot.reply_to(message, "⚠️ Пожалуйста, выберите категорию из списка")
            logger.warning(f"Invalid category choice from user {message.from_user.id}: {message.text}")
            self.handle_add_dish(message)  # Перезапускаем процесс
        except Exception as e:
            self.bot.reply_to(message, f"❌ Ошибка: {str(e)}")
            logger.error(f"Category choice error from user {message.from_user.id}: {e}")

    def handle_add_dish(self, message):
        try:
            from storage.category_storage import get_categories

            categories = get_categories()
            if not categories:
                self.bot.reply_to(message,
                                  "❌ Нет доступных категорий. Сначала создайте категорию через /addcategory")
                return

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            for cat in categories:
                markup.add(f"{cat.id}. {cat.name}")

            msg = self.bot.reply_to(message, "Выберите категорию:", reply_markup=markup)
            self.bot.register_next_step_handler(msg, self.process_category_choice)

        except Exception as e:
            self.bot.reply_to(message, f"❌ Ошибка: {str(e)}")
            logger.error(f"Add dish init error from user {message.from_user.id}: {e}")



def check_tables():
    init_db()
    inspector = inspect(engine)
    print("Таблицы в БД:", inspector.get_table_names())

check_tables()


def main():
    try:
        # Инициализация БД (без пересоздания таблиц)
        init_db()
        check_tables()

        bot = telebot.TeleBot(TG_API_KEY)

        # Инициализация обработчика блюд
        dish_handler = DishHandler(bot)

        # Регистрация обработчика
        @bot.message_handler(commands=['adddish'])
        def add_dish_wrapper(message):
            logger.info(f"User {message.from_user.id} started /adddish command")
            dish_handler.handle_add_dish(message)



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


        @bot.message_handler(commands=['dishes'])
        def handle_list_dishes(message):
            from storage.category_storage import get_categories
            from storage.dish_storage import get_dishes_by_category

            try:
                # Получаем список всех категорий
                categories = get_categories()
                if not categories:
                    bot.reply_to(message, "Сначала создайте категории через /addcategory")
                    return

                # Создаем клавиатуру с категориями
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                for category in categories:
                    markup.add(f"{category.id}. {category.name}")

                # Просим выбрать категорию
                msg = bot.reply_to(message, "Выберите категорию для просмотра блюд:", reply_markup=markup)
                bot.register_next_step_handler(msg, lambda m: process_category_choice(m, categories))

            except Exception as e:
                bot.reply_to(message, f"❌ Ошибка: {str(e)}")
                logger.error(f"Error in /dishes command: {e}")

        def process_category_choice(message, categories):
            try:
                from storage.dish_storage import get_dishes_by_category

                # Парсим выбор пользователя
                try:
                    selected_id = int(message.text.split('.')[0])
                except (ValueError, IndexError):
                    raise ValueError("Пожалуйста, выберите категорию из списка")

                # Проверяем, что выбранная категория существует
                selected_category = next((cat for cat in categories if cat.id == selected_id), None)
                if not selected_category:
                    raise ValueError("Выбранная категория не найдена")

                # Получаем блюда для выбранной категории
                dishes = get_dishes_by_category(selected_id)

                # Формируем ответ
                if dishes:
                    response = [f"🍽 Блюда в категории '{selected_category.name}':"]
                    for dish in dishes:
                        dish_info = f"  - {dish.name}: {dish.price} руб."
                        if dish.description:
                            dish_info += f" ({dish.description})"
                        response.append(dish_info)
                    bot.reply_to(message, "\n".join(response), reply_markup=types.ReplyKeyboardRemove())
                else:
                    bot.reply_to(message, f"В категории '{selected_category.name}' пока нет блюд",
                                 reply_markup=types.ReplyKeyboardRemove())

            except ValueError as e:
                bot.reply_to(message, f"⚠️ {str(e)}")
                logger.warning(f"Invalid category choice: {message.text}")
            except Exception as e:
                bot.reply_to(message, "❌ Произошла ошибка при получении блюд")
                logger.error(f"Error showing dishes: {e}")


        def show_dishes_by_category(message):
            try:
                from storage.dish_storage import get_dishes_by_category

                # Парсим выбор пользователя
                category_id = int(message.text.split('.')[0])

                # Получаем блюда для выбранной категории
                dishes = get_dishes_by_category(category_id)

                if dishes:
                    response = "\n".join([
                        f"{d.id}. {d.name} - {d.price} руб." +
                        (f" ({d.description})" if d.description else "") +
                        (f"\n  🖼: {d.image_url}" if d.image_url else "")
                        for d in dishes
                    ])
                    bot.reply_to(message, f"🍽 Блюда в этой категории:\n{response}",
                                 reply_markup=types.ReplyKeyboardRemove())
                else:
                    bot.reply_to(message, "В этой категории пока нет блюд",
                                 reply_markup=types.ReplyKeyboardRemove())

            except (ValueError, IndexError):
                bot.reply_to(message, "⚠️ Пожалуйста, выберите категорию из списка")
                logger.warning(f"Invalid category choice: {message.text}")
            except Exception as e:
                bot.reply_to(message, "❌ Произошла ошибка при получении блюд")
                logger.error(f"Error showing dishes: {e}")

        @bot.message_handler(commands=['all_dishes'])
        def handle_all_dishes(message):
            try:
                from storage.dish_storage import get_all_dishes_with_categories
                dishes_categories = get_all_dishes_with_categories()

                if not dishes_categories:
                    bot.reply_to(message, "🍽 Блюд пока нет")
                    return

                # Группируем по категориям
                from collections import defaultdict
                grouped = defaultdict(list)
                for dish, category in dishes_categories:
                    grouped[category.name].append(dish)

                # Формируем красивый ответ
                response = ["📋 <b>Все блюда в меню:</b>"]
                for category_name, dishes in grouped.items():
                    dish_list = []
                    for dish in dishes:
                        dish_info = f"  - {dish.name} - {dish.price} руб."
                        if dish.description:
                            dish_info += f" ({dish.description})"
                        dish_list.append(dish_info)

                    response.append(f"\n🍽 <b>{category_name}:</b>\n" + "\n".join(dish_list))

                bot.reply_to(message, "\n".join(response), parse_mode='HTML')

            except Exception as e:
                bot.reply_to(message, "❌ Произошла ошибка при получении списка блюд")
                logger.error(f"Error in all_dishes handler: {e}")


        @bot.message_handler(commands=['start'])
        def handle_start(message):
            from models.user import User
            from storage.user_storage import add_user, get_user_by_telegram_id
            import time

            try:
                # Проверяем, есть ли пользователь уже в БД
                existing_user = get_user_by_telegram_id(message.from_user.id)
                if existing_user:
                    bot.reply_to(message, "👋 Вы уже зарегистрированы!")
                    return

                # Задержка для защиты от спама
                time.sleep(0.5)

                user = User(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name
                )
                add_user(user)

                welcome_text = """
        👋 <b>Добро пожаловать в FoodNinja!</b>

        Я помогу вам управлять меню вашего ресторана или кафе.

        📌 Основные команды:
        /help - Показать все доступные команды
        /adddish - Добавить новое блюдо
        /dishes - Просмотреть меню в выбранной категории
        /all_dishes - Посмотреть весь ассортимент блюд
        /ping - Проверь коннект с сервером

        Начните с добавления категорий через /addcategory, затем добавляйте блюда через /adddish.
                """
                bot.reply_to(message, welcome_text, parse_mode='HTML')

            except Exception as e:
                logger.error(f"Ошибка регистрации: {e}")
                time.sleep(1)  # Добавляем задержку при ошибке
                bot.reply_to(message, "🔁 Проблема с регистрацией. Попробуйте снова через минуту.")


        @bot.message_handler(commands=['help'])
        def handle_help(message):
            logger.info(f"User {message.from_user.id} requested help")
            commands = {
                '🍽 Меню': [
                    ('/addcategory', 'Добавить категорию блюд'),
                    ('/categories', 'Просмотреть категории'),
                    ('/adddish', 'Добавить новое блюдо'),
                    ('/dishes', 'Просмотреть блюда в выбранной категории'),
                    ('/all_dishes', 'Посмотреть весь ассортимент блюд')
                ],
                '🛠 Управление': [
                    ('/start', 'Перезапустить бота'),
                    ('/help', 'Помощь по командам'),
                    ('/ping', 'Проверь коннект с сервером')
                ]
            }

            help_text = "<b>🍴 FoodNinja Bot - Список команд</b>\n\n"

            for section, cmds in commands.items():
                help_text += f"<b>{section}:</b>\n"
                help_text += "\n".join([f"{cmd[0]} - {cmd[1]}" for cmd in cmds])
                help_text += "\n\n"

            bot.reply_to(message, help_text, parse_mode='HTML')

        @bot.message_handler(commands=['ping'])
        def ping(message):
            try:
                bot.reply_to(message, "🏓 Pong!")
            except Exception as e:
                logger.error(f"Connection error: {e}")

        # Запуск бота


        logger.info("Бот запущен")
        bot.infinity_polling(long_polling_timeout=10)

    except Exception as e:
        logger.error(f"Ошибка в main: {e}")
        raise

if __name__ == "__main__":
    main()
    try:
        # Удерживаем выполнение, чтобы бот работал
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Бот остановлен.")

