from datetime import datetime
from models.order import Order
from typing import Optional, List, TYPE_CHECKING
from models.enums import OrderStatus, PaymentMethod

if TYPE_CHECKING:
    from models.order import Order
    from storage.db_session import DBSession
    from models.enums import OrderStatus, PaymentMethod








if TYPE_CHECKING:
    from storage.db_session import DBSession


class OrderStorage:
    def __init__(self, db_session: 'DBSession', sql_data: dict[str, str]) -> None:
        self._db_session = db_session
        self._sql_data = sql_data
        self._init_table()

    def _init_table(self) -> None:
        table_name = self._sql_data.get("tables", {}).get("orders", "orders")
        with self._db_session.get_session() as conn:
            conn.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    payment_method TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            conn.commit()


    def save(self, order: Order) -> Order:
        if not isinstance(order.status, OrderStatus):
            raise TypeError("order.status must be OrderStatus enum")
        if order.payment_method is not None and not isinstance(order.payment_method, PaymentMethod):
            raise TypeError("order.payment_method must be PaymentMethod enum or None")
        with self._db_session.get_session() as conn:
            if order.id == 0:
                cursor = conn.execute(
                    f"INSERT INTO {self._sql_data['tables']['orders']} "
                    "(user_id, status, payment_method) VALUES (?, ?, ?)",
                    (order.user_id, order.status.value, order.payment_method.value if order.payment_method else None)
                )
                order._id = cursor.lastrowid
            else:
                conn.execute(
                    f"UPDATE {self._sql_data['tables']['orders']} SET "
                    "user_id=?, status=?, payment_method=? WHERE id=?",
                    (order.user_id, order.status.value, order.payment_method.value if order.payment_method else None,
                     order.id)
                )
            conn.commit()  # Важно: явный коммит!
        return order

    def load_by_id(self, id: int) -> Optional[Order]:
        with self._db_session.get_session() as conn:
            row = conn.execute(
                f'''
                SELECT id, user_id, status, payment_method, created_at
                FROM {self._sql_data["tables"]["orders"]}
                WHERE id = ?
                ''',
                (id,)
            ).fetchone()
            if not row:
                return None

            try:
                status = OrderStatus(row[2])
                payment_method = PaymentMethod(row[3]) if row[3] else None
                created_at = datetime.fromisoformat(row[4])
            except ValueError as e:
                raise ValueError(
                    f"Invalid data in database for order {id}: "
                    f"status={row[2]}, payment_method={row[3]}, created_at={row[4]}. "
                    f"Error: {e}"
                )

            return Order(
                id=row[0],
                user_id=row[1],
                status=status,
                payment_method=payment_method,
                created_at=created_at
            )

    def load_by_user(self, user_id: int) -> List['Order']:
        with self._db_session.get_session() as conn:
            rows = conn.execute(
                f'''
                SELECT id, user_id, status, payment_method, created_at 
                FROM {self._sql_data["tables"]["orders"]} 
                WHERE user_id = ?
                ''',
                (user_id,)
            ).fetchall()

            orders = []
            for row in rows:
                try:
                    status = OrderStatus(row[2])
                    payment_method = PaymentMethod(row[3]) if row[3] else None
                    created_at = datetime.fromisoformat(row[4])
                    orders.append(Order(
                        id=row[0],
                        user_id=row[1],
                        status=status,
                        payment_method=payment_method,
                        created_at=created_at
                    ))
                except ValueError as e:
                    raise ValueError(
                        f"Invalid data in database for order {row[0]}: "
                        f"status={row[2]}, payment_method={row[3]}, created_at={row[4]}. "
                        f"Error: {e}"
                    )
            return orders