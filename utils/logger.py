import logging
from pathlib import Path
from datetime import datetime
import os
import logging
import sys

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Создаем обработчик с правильной кодировкой
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    ))

    # Добавляем обработчик только если его еще нет
    if not logger.handlers:
        logger.addHandler(handler)

    return logger


