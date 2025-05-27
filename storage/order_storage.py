
from datetime import datetime
from typing import List, Optional, cast

from models.enums import OrderStatus, PaymentMethod
from models.order import Order
from storage.db_session import DBSession


class OrderStorage:
    def __init__(self, db_session: 'DBSession', sql_data: dict[str, str]) -> None:
        self._db_session = db_session
        self._sql_data = sql_data
        self._init_table()

    def _init_table(self) -> None:
        """Создаёт таблицу для хранения заказов, если она не существует."""
        conn = self._db_session.get_session()
        cursor = conn.cursor()
        table_name: str = self._sql_data['orders_table_name']
        cursor.execute(
            f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    payment_method TEXT
                )
            """
        )
        conn.commit()
        conn.close()

    def save(self, order: 'Order') -> None:
        """Сохраняет объект Order в базу данных. Если запись с таким id существует — обновляет её."""
        conn = self._db_session.get_session()
        cursor = conn.cursor()
        table_name: str = self._sql_data['orders_table_name']
        cursor.execute(
            f"""
                INSERT OR REPLACE INTO {table_name} (
                    id, user_id, status, created_at, payment_method
                ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                order.id,
                order.user_id,
                order.status.name,
                order.created_at.isoformat(),
                order.payment_method.name if order.payment_method else None
            )
        )
        conn.commit()
        conn.close()

    def del_by_id(self, order_id: int) -> None:
        """Удаляет заказ по его id."""
        conn = self._db_session.get_session()
        cursor = conn.cursor()
        table_name: str = self._sql_data['orders_table_name']
        cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (order_id,))
        conn.commit()
        conn.close()

    def load_all(self) -> List['Order']:
        """Загружает все заказы из базы данных."""
        conn = self._db_session.get_session()
        cursor = conn.cursor()
        table_name: str = self._sql_data['orders_table_name']
        items_table_name: str = self._sql_data['order_items_table_name']
        cursor.execute(
            f"SELECT id, user_id, status, created_at, payment_method FROM {table_name}"
        )
        rows = cursor.fetchall()
        orders: List[Order] = []
        conn.close()
        for id_, user_id, status_str, created_at_str, payment_method_str in rows:
            status: OrderStatus = cast(OrderStatus, OrderStatus[status_str])
            created_at: datetime = datetime.fromisoformat(created_at_str)
            payment_method: Optional[PaymentMethod] = (
                PaymentMethod[payment_method_str] if payment_method_str else None
            )
            orders.append(Order(id_, user_id, status, created_at, payment_method))
        return orders

