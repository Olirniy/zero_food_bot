
from typing import List, Optional
from storage.db_session import DBSession
from models.dish import Dish


class DishStorage:
    def __init__(self, db_session: 'DBSession', sql_data: dict[str, str]) -> None:
        self._db_session = db_session
        self._sql_data = sql_data
        self._init_table()

    def _init_table(self) -> None:
        """Создаёт таблицу блюд, если она не существует."""
        conn = self._db_session.get_session()
        cursor = conn.cursor()
        table_name: str = self._sql_data['dishes_table_name']
        cursor.execute(
            f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY,
                    category_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    short_description TEXT NOT NULL,
                    description TEXT NOT NULL,
                    price REAL NOT NULL,
                    photo_url TEXT
                )
            """
        )
        conn.commit()

    def load_all(self) -> List[Dish]:
        """Загружает все блюда из базы данных."""
        conn = self._db_session.get_session()
        cursor = conn.cursor()
        table_name: str = self._sql_data['dishes_table_name']
        cursor.execute(
            f"SELECT id, category_id, name, short_description, description, price, photo_url FROM {table_name}"
        )
        rows = cursor.fetchall()
        conn.close()
        return [
            Dish(
                id=row[0],
                category_id=row[1],
                name=row[2],
                short_description=row[3],
                description=row[4],
                price=row[5],
                photo_url=row[6]
            )
            for row in rows
        ]

    def save_all(self, dishes: List[Dish]) -> None:
        """Сохраняет список блюд в БД, используя INSERT OR REPLACE для каждой записи."""
        conn = self._db_session.get_session()
        cursor = conn.cursor()
        table_name: str = self._sql_data['dishes_table_name']
        cursor.executemany(
            f"""
                INSERT OR REPLACE INTO {table_name} (
                    id, category_id, name, short_description, description, price, photo_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    dish.id,
                    dish.category_id,
                    dish.name,
                    dish.short_description,
                    dish.description,
                    dish.price,
                    dish.photo_url
                )
                for dish in dishes
            ]
        )
        conn.commit()
        conn.close()

    def del_all(self) -> None:
        """Удаляет все записи из таблицы блюд."""
        conn = self._db_session.get_session()
        cursor = conn.cursor()
        table_name: str = self._sql_data['dishes_table_name']
        cursor.execute(f"DELETE FROM {table_name}")
        conn.commit()
        conn.close()

