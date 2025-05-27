
from typing import Optional, List

from models.category import Category
from storage.db_session import DBSession


class CategoryStorage:
    def __init__(self, db_session: DBSession, sql_data: dict[str, str]) -> None:
        """
        :param db_session: объект сессии базы данных
        :param sql_data: словарь с именем таблицы категорий и другими SQL-конфигурациями
        """
        self._db_session: DBSession = db_session
        self._sql_data: dict[str, str] = sql_data  # данные по названиям таблиц, путям к БД и т.п.
        self._init_table()

    def _init_table(self) -> None:
        """Создаёт таблицу категорий, если она не существует."""
        table: str = self._sql_data['categories_table_name']
        conn = self._db_session.get_session()
        conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()

    def save(self, category: Category) -> None:
        """
        Сохраняет категорию в БД.
        Использует INSERT OR REPLACE для обновления или вставки одной командой.
        """
        conn = self._db_session.get_session()
        table: str = self._sql_data['categories_table_name']
        conn.execute(
            f"""
            INSERT OR REPLACE INTO {table} (
                id, name
            ) VALUES (?, ?)
            """,
            (category.id, category.name)
        )
        conn.commit()
        conn.close()

    def load_all(self) -> List[Category]:
        """
        Загружает все категории из таблицы.
        :return: список объектов Category.
        """
        table: str = self._sql_data['categories_table_name']
        conn = self._db_session.get_session()
        cursor = conn.execute(f"SELECT id, name FROM {table}")
        rows = cursor.fetchall()
        conn.close()
        return [Category(id=row[0], name=row[1]) for row in rows]


    def del_all(self) -> None:
        """
        Удаляет все записи из таблицы категорий.
        """
        table: str = self._sql_data['categories_table_name']
        conn = self._db_session.get_session()
        conn.execute(f"DELETE FROM {table}")
        conn.commit()
        conn.close()


