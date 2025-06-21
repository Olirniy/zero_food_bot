from telebot import TeleBot
from storage.db_session import DBSession
from core.handlers.base import register_base_handlers
from core.handlers.menu import register_menu_handlers
from core.handlers.cart import register_cart_handlers
from config import TG_API_KEY, SQL_DATA
from utils.init_data import init_sample_data
import os  # Добавлено
from utils.dependencies import log_dependencies
log_dependencies()
from utils.logger import setup_logger  # Добавить в импорты

logger = setup_logger(__name__)  # После всех импортов



def main():
    logger.info("Запуск бота")
    try:
        # Создаем папку data если её нет
        os.makedirs('data', exist_ok=True)

        # Инициализация БД
        db = DBSession()
        print(f"🛢 Используется БД: {SQL_DATA['db_path']}")
        print("Существует ли файл БД:", os.path.exists(SQL_DATA['db_path']))




        # Запись всех таблиц БД
        with db.get_session() as conn:
            tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            logger.info(f"Таблицы БД: {tables}")


        # Создаем бота
        bot = TeleBot(TG_API_KEY)
        print("Проверка токена:", bool(TG_API_KEY))

        # Регистрация обработчиков
        register_base_handlers(bot, db, SQL_DATA)
        register_menu_handlers(bot, db, SQL_DATA)
        register_cart_handlers(bot, db, SQL_DATA)

        print("🍜 Бот запущен и ожидает сообщений...")
        bot.infinity_polling()
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}", exc_info=True)

if __name__ == "__main__":
    main()
