import json
import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

# Основной токен (обязательный)
TG_API_KEY = os.getenv("ZERO_FOOD_BOT_API_KEY")

if not TG_API_KEY:
    raise ValueError("Токен бота не найден! Добавьте ZERO_FOOD_BOT_API_KEY в .env файл")



def load_config():
    #Загружаем конфиг из файла
    with open("config.json", "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
    load_dotenv(".env")
    config["tg_api_key"] = os.getenv("ZERO_FOOD_BOT_API_KEY")
    config["debug_tg_api_key"] = os.getenv("ZERO_FOOD_BOT_API_KEY_DEBUG")
    return config

config = load_config()
TG_API_KEY = config["tg_api_key"]
ADMINS = config["admins"]
LOGS_DIRECTORY = config["logs_directory"]
debug_mode = config["debug_mode"]
if debug_mode==1:
    TG_API_KEY = config["debug_tg_api_key"]
    LOGS_DIRECTORY = config["logs_directory_deb"]