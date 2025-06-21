from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from repository.category_repo import CategoryRepository
from repository.dish_repo import DishRepository
from storage.category_storage import CategoryStorage  # Добавляем импорт
from storage.dish_storage import DishStorage
from utils.logger import setup_logger  # Добавить в импорты
logger = setup_logger(__name__)  # После всех импортов
logger.debug(f"Импортирован {__name__}")



# Добавляем импорт

def register_menu_handlers(bot: TeleBot, db, sql_data: dict):
    category_storage = CategoryStorage(db, sql_data)
    dish_storage = DishStorage(db, sql_data)
    category_repo = CategoryRepository(category_storage)
    dish_repo = DishRepository(dish_storage)

    @bot.message_handler(commands=['menu'])
    def show_categories(message: Message):
        try:
            categories = category_repo.get_all()

            if not categories:
                bot.reply_to(message, "🍽 Меню пока пусто")
                return

            markup = InlineKeyboardMarkup(row_width=2)
            buttons = [InlineKeyboardButton(cat.name, callback_data=f"cat_{cat.id}") for cat in categories]
            markup.add(*buttons)

            bot.send_message(
                message.chat.id,
                "🍜 *Выберите категорию:*",
                reply_markup=markup,
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Ошибка в меню: {e}")
            bot.reply_to(message, "❌ Ошибка при загрузке меню")

    @bot.callback_query_handler(func=lambda call: call.data.startswith('cat_'))
    def show_dishes(call: CallbackQuery):
        try:
            category_id = int(call.data.split('_')[1])
            dishes = dish_repo.get_by_category(category_id)

            if not dishes:
                bot.answer_callback_query(call.id, "🍽 В этой категории пока нет блюд")
                return

            # Отправляем сообщение с категорией
            category = category_repo.get_by_id(category_id)
            bot.send_message(
                call.message.chat.id,
                f"🍜 *{category.name}:*",
                parse_mode="Markdown"
            )

            # Отправляем блюда
            for dish in dishes:
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton(
                    "➕ Добавить в корзину",
                    callback_data=f"add_{dish.id}"
                ))

                caption = f"🍽 *{dish.name}*\n{dish.short_description}\nЦена: {dish.price}₽"

                if dish.photo_url:
                    try:
                        bot.send_photo(
                            call.message.chat.id,
                            photo=open(dish.photo_url, 'rb'),
                            caption=caption,
                            reply_markup=markup,
                            parse_mode="Markdown"
                        )
                    except:
                        bot.send_message(
                            call.message.chat.id,
                            caption,
                            reply_markup=markup,
                            parse_mode="Markdown"
                        )
                else:
                    bot.send_message(
                        call.message.chat.id,
                        caption,
                        reply_markup=markup,
                        parse_mode="Markdown"
                    )

        except Exception as e:
            logger.error(f"Ошибка при показе блюд: {e}", exc_info=True)
            bot.answer_callback_query(call.id, "❌ Ошибка при загрузке блюд")