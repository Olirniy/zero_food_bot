# models/payment.py
from datetime import datetime
from typing import Optional
from models.enums import PaymentStatus  # Добавляем импорт


class Payment:
    def __init__(self,
                 id: int,
                 order_id: int,
                 amount: float,
                 method: str,
                 status: PaymentStatus,  # Используем enum
                 transaction_id: Optional[str] = None,
                 created_at: Optional[datetime] = None):
        self._id = id
        self._order_id = order_id
        self._amount = amount
        self._method = method
        self._status = status
        self._transaction_id = transaction_id
        self._created_at = created_at or datetime.now()



    @property
    def id(self) -> int:
        return self._id

    @property
    def order_id(self) -> int:
        return self._order_id

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def method(self) -> str:
        return self._method

    @property
    def status(self) -> PaymentStatus:
        return self._status

    @status.setter
    def status(self, value: PaymentStatus):
        self._status = value

    @property
    def transaction_id(self) -> Optional[str]:
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, value: str):
        self._transaction_id = value

    @property
    def created_at(self) -> datetime:
        return self._created_at