
import sqlite3
from sqlite3 import Connection

class DBSession:
    def __init__(self, db_path: str) -> None:
        """Инициализирует подключение к базе данных SQLite по указанному пути."""
        self._db_path: str = db_path

    def get_session(self) -> Connection:
        """Возвращает текущую сессию (соединение) с базой данных."""
        return sqlite3.connect(self._db_path)


