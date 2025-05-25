from typing import List, Optional
from models.payment import Payment, PaymentStatus
from storage.db_session import DBSession


class PaymentStorage:
    def __init__(self, db_session: DBSession, sql_data: dict):
        self._db_session = db_session
        self._sql_data = sql_data
        self._init_table()

    def _init_table(self):
        with self._db_session.get_session() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    amount REAL NOT NULL,
                    method TEXT NOT NULL,
                    status TEXT NOT NULL,
                    transaction_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (order_id) REFERENCES orders(id)
                )
            ''')
            conn.commit()

    def save(self, payment: Payment) -> Payment:
        with self._db_session.get_session() as conn:
            if payment.id == 0:  # Новый платеж
                cursor = conn.execute('''
                    INSERT INTO payments 
                    (order_id, amount, method, status, transaction_id)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    payment.order_id,
                    payment.amount,
                    payment.method,
                    payment.status.value,
                    payment.transaction_id
                ))
                payment._id = cursor.lastrowid
            else:  # Обновление
                conn.execute('''
                    UPDATE payments SET
                    order_id = ?,
                    amount = ?,
                    method = ?,
                    status = ?,
                    transaction_id = ?
                    WHERE id = ?
                ''', (
                    payment.order_id,
                    payment.amount,
                    payment.method,
                    payment.status.value,
                    payment.transaction_id,
                    payment.id
                ))
            conn.commit()
        return payment

    def load_by_order(self, order_id: int) -> List[Payment]:
        with self._db_session.get_session() as conn:
            rows = conn.execute('''
                SELECT id, order_id, amount, method, status, 
                       transaction_id, created_at
                FROM payments
                WHERE order_id = ?
            ''', (order_id,)).fetchall()

            payments = []
            for row in rows:
                payments.append(Payment(
                    id=row[0],
                    order_id=row[1],
                    amount=row[2],
                    method=row[3],
                    status=PaymentStatus(row[4]),
                    transaction_id=row[5],
                    created_at=row[6]
                ))
            return payments