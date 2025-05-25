from datetime import datetime
from typing import Optional

from models.enums import OrderStatus, PaymentMethod
from models.order_item import OrderItem


class Order:
    def __init__(self, id: int, user_id: int, status: OrderStatus, created_at: datetime, payment_method: Optional[PaymentMethod]):
        self._id = id
        self._user_id = user_id
        self._status = status
        self._payment_method = payment_method
        self._created_at = created_at
        self._items: list[OrderItem] = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def status(self) -> OrderStatus:
        return self._status

    @status.setter
    def status(self, status: OrderStatus):
        if not isinstance(status, OrderStatus):
            raise TypeError("status must be OrderStatus enum")
        self._status = status

    @property
    def payment_method(self) -> PaymentMethod | None:
        return self._payment_method

    @payment_method.setter
    def payment_method(self, payment_method: Optional[PaymentMethod]):
        if payment_method is not None and not isinstance(payment_method, PaymentMethod):
            raise TypeError("payment_method must be PaymentMethod enum or None")
        self._payment_method = payment_method

    @property
    def created_at(self) -> datetime:
        return self._created_at

    def add_item(self, item: OrderItem):
        self._items.append(item)

    def del_item(self, item: OrderItem):
        pass