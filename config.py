
import json
import os
from dotenv import load_dotenv

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
ADMIN_GROUP_ID = config["admin_group_id"]
DEFAULT_IMG_PATH = config["default_img"]

LOGS_DIRECTORY = config["logs_directory"]
SQL_DATA = {"db_path": config["db_path"],
            "orders_table_name": config["orders_table_name"],
            "feedback_table_name": config["feedback_table_name"],
            "order_items_table_name": config["order_items_table_name"],
            "dishes_table_name": config["dishes_table_name"],
            "categories_table_name": config["categories_table_name"]}
debug_mode = config["debug_mode"]


if debug_mode==1:
    TG_API_KEY = config["debug_tg_api_key"]
    LOGS_DIRECTORY = config["logs_directory_deb"]

