
from typing import List
from models.order_item import OrderItem
from storage.db_session import DBSession


class OrderItemStorage:
    def __init__(self, db_session: 'DBSession', sql_data: dict[str, str]) -> None:
        self._db_session = db_session
        self._sql_data = sql_data
        self._init_table()

    def _init_table(self) -> None:
        """Создаёт таблицу для хранения позиций заказа, если она не существует."""
        conn = self._db_session.get_session()
        cursor = conn.cursor()
        table_name: str = self._sql_data['order_items_table_name']
        cursor.execute(
            f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY,
                    order_id INTEGER NOT NULL,
                    dish_id INTEGER NOT NULL,
                    dish_name TEXT NOT NULL,
                    dish_price REAL NOT NULL,
                    quantity INTEGER NOT NULL
                )
            """
        )
        conn.commit()
        conn.close()

    def save(self, item: 'OrderItem') -> None:
        """Сохраняет объект OrderItem в базу данных. Если запись с таким id существует — обновляет её."""
        conn = self._db_session.get_session()
        cursor = conn.cursor()
        table_name: str = self._sql_data['order_items_table_name']
        cursor.execute(
            f"""
                INSERT OR REPLACE INTO {table_name} (
                    id, order_id, dish_id, dish_name, dish_price, quantity
                ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                item.id,
                item.order_id,
                item.dish_id,
                item.dish_name,
                item.dish_price,
                item.quantity
            )
        )
        conn.commit()
        conn.close()

    def delete(self, item_id: int) -> None:
        """Удаляет позицию заказа по её id."""
        conn = self._db_session.get_session()
        cursor = conn.cursor()
        table_name: str = self._sql_data['order_items_table_name']
        cursor.execute(
            f"DELETE FROM {table_name} WHERE id = ?",
            (item_id,)
        )
        conn.commit()
        conn.close()

    def load_all(self) -> List['OrderItem']:
        """Загружает все позиции заказов из базы данных."""
        conn = self._db_session.get_session()
        cursor = conn.cursor()
        table_name: str = self._sql_data['order_items_table_name']
        cursor.execute(
            f"SELECT id, order_id, dish_id, dish_name, dish_price, quantity FROM {table_name}"
        )
        rows = cursor.fetchall()
        conn.close()
        return [
            OrderItem(
                id=row[0],
                order_id=row[1],
                dish_id=row[2],
                dish_name=row[3],
                dish_price=row[4],
                quantity=row[5]
            )
            for row in rows
        ]

    def load_by_order(self, order_id: int) -> List['OrderItem']:
        """Загружает все позиции заказа по указанному order_id."""
        conn = self._db_session.get_session()
        cursor = conn.cursor()
        table_name: str = self._sql_data['order_items_table_name']
        cursor.execute(
            f"""
                SELECT id, order_id, dish_id, dish_name, dish_price, quantity
                FROM {table_name}
                WHERE order_id = ?
            """,
            (order_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [
            OrderItem(
                id=row[0],
                order_id=row[1],
                dish_id=row[2],
                dish_name=row[3],
                dish_price=row[4],
                quantity=row[5]
            )
            for row in rows
        ]

