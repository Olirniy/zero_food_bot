from telebot import TeleBot
from telebot.types import Message
from repository.user_repo import UserRepository
from storage.user_storage import UserStorage
from utils.logger import setup_logger  # Добавить в импорты
logger = setup_logger(__name__)  # После всех импортов
logger.debug(f"Импортирован {__name__}")



def register_base_handlers(bot: TeleBot, db, sql_data: dict):
    user_repo = UserRepository(UserStorage(db, sql_data))

    @bot.message_handler(commands=['start'])
    def handle_start(message: Message):
        user = user_repo.get_or_create(
            telegram_id=message.from_user.id,
            username=message.from_user.username or f"user_{message.from_user.id}"
        )
        bot.reply_to(message, f"👋 {'Новый пользователь' if user.id == 0 else 'С возвращением'}, {user.username}!")

    @bot.message_handler(commands=['help'])
    def handle_help(message: Message):
        bot.reply_to(message, "ℹ️ Доступные команды:\n/start - регистрация\n/menu - показать меню")