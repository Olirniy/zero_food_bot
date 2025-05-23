import sqlite3
import os
import threading
from config import SQL_DATA


class DBSession:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.db_path = os.path.abspath(SQL_DATA["db_path"])
                    cls._instance.local = threading.local()
                    cls._instance._initialized = False
        return cls._instance

    def get_session(self) -> sqlite3.Connection:
        if not hasattr(self.local, 'conn') or self.local.conn is None:
            self.local.conn = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
                timeout=30.0
            )

            if not self._initialized:
                self._init_tables()
                self._initialized = True

        return self.local.conn

    def _init_tables(self):
        """Создает все таблицы при первом подключении"""
        tables_sql = [
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                username TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )""",
            """CREATE TABLE IF NOT EXISTS dishes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                short_description TEXT,
                description TEXT,
                price REAL NOT NULL,
                photo_url TEXT,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )"""
        ]

        conn = self.local.conn
        for table_sql in tables_sql:
            try:
                conn.execute(table_sql)
            except sqlite3.Error as e:
                print(f"Error creating table: {e}")
        conn.commit()

    def close(self):
        if hasattr(self.local, 'conn') and self.local.conn:
            self.local.conn.close()
            self.local.conn = None
