# config.py
import json
import os
from dotenv import load_dotenv


def load_config():
    # Загружаем конфиг из файла
    with open("config.json", "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
    load_dotenv(".env")
    config["tg_api_key"] = os.getenv("ZERO_FOOD_BOT_API_KEY")
    config["debug_tg_api_key"] = os.getenv("ZERO_FOOD_BOT_API_KEY_DEBUG")

    # Определяем путь к БД в зависимости от режима
    db_path = 'test.db' if os.getenv('TEST_MODE') == '1' else 'bot.db'

    # Добавляем данные для БД
    # В функции load_config() добавьте:
    config["SQL_DATA"] = {
        "db_path": db_path,
        "tables": {
            "users": "users",
            "categories": "categories",
            "dishes": "dishes",
            "orders": "orders",
            "order_items": "order_items",
            "feedback": "feedback"  # Добавьте эту строку
        }
    }
    return config


config = load_config()
TG_API_KEY = config["tg_api_key"]
ADMINS = config["admins"]
LOGS_DIRECTORY = config["logs_directory"]
SQL_DATA = config["SQL_DATA"]  # Добавляем экспорт SQL_DATA

debug_mode = config["debug_mode"]
if debug_mode == 1:
    TG_API_KEY = config["debug_tg_api_key"]
    LOGS_DIRECTORY = config["logs_directory_deb"]