import os
import logging
import telebot
from storage.db_session import DBSession
from storage.user_storage import UserStorage
from models.user import User
from config import TG_API_KEY, SQL_DATA
import sqlite3



# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    try:
        # Удаляем старые файлы БД
        if os.path.exists(SQL_DATA["db_path"]):
            try:
                os.remove(SQL_DATA["db_path"])
                print("Удалена старая БД")
            except Exception as e:
                print(f"Не удалось удалить БД: {e}")

        # Инициализация БД (создаст таблицы при первом вызове)
        db = DBSession()

        # Явная проверка таблиц
        with db.get_session() as conn:
            tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            print(f"Таблицы в БД: {[t[0] for t in tables]}")

            # Если нет таблиц - создаем заново
            if not tables:
                db._init_tables()
                print("Таблицы созданы принудительно")

        # Остальной код бота...
        user_storage = UserStorage(db, SQL_DATA)
        bot = telebot.TeleBot(TG_API_KEY)

        @bot.message_handler(commands=['start'])
        def handle_start(message):
            try:
                # Проверка таблицы users
                with db.get_session() as conn:
                    conn.execute("SELECT 1 FROM users LIMIT 1")

                user = user_storage.load_by_telegram_id(message.from_user.id)
                if not user:
                    new_user = User(
                        id=0,
                        telegram_id=message.from_user.id,
                        username=message.from_user.username or f"user_{message.from_user.id}"
                    )
                    user_storage.save(new_user)
                    user = user_storage.load_by_telegram_id(message.from_user.id)
                    bot.reply_to(message, f"✅ Регистрация успешна! ID: {user.id}")
                else:
                    bot.reply_to(message, f"👋 С возвращением! ID: {user.id}")
            except sqlite3.OperationalError as e:
                print(f"Ошибка таблицы users: {e}")
                bot.reply_to(message, "❌ Ошибка БД. Перезапустите бота.")

        logger.info("Starting bot...")
        bot.infinity_polling()



    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()