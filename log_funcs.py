from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime
import sys
import logging
from logging.handlers import RotatingFileHandler


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(
        'logs/bot_errors.log',
        maxBytes=5 * 1024 * 1024,
        backupCount=3
    )
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

try:
    # Получаем абсолютный путь к директории проекта
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_DIR = os.path.join(BASE_DIR, 'logs')

    # Создаем папку logs (с дополнительными проверками)
    if not os.path.exists(LOG_DIR):
        try:
            os.makedirs(LOG_DIR)
        except FileExistsError:
            pass  # Папка уже существует (многопоточная конкуренция)
        except Exception as e:
            print(f"FATAL: Cannot create logs directory: {e}")
            sys.exit(1)

    # Настройка логгера
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Формат сообщений
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Файловый обработчик
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(LOG_DIR, 'foodbot.log'),
        when='midnight',
        backupCount=7,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Добавляем обработчики
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("Logger successfully configured")

except Exception as e:
    print(f"CRITICAL: Failed to initialize logger: {e}")
    raise