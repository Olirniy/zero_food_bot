from datetime import datetime
from typing import Optional
from models.enums import OrderStatus, PaymentMethod
from models.order_item import OrderItem




class Order:
    """Модель заказа"""
    def __init__(self, id: int, user_id: int, status: OrderStatus,
                 payment_method: Optional[PaymentMethod], created_at: datetime):
        # Заменяем self.id = id на self._id = id
        self._id = id
        self._user_id = user_id
        self._status = status
        self._payment_method = payment_method
        self._created_at = created_at
        self._items: list[OrderItem] = []


    # Добавляем методы для работы с заказами
    def __repr__(self) -> str:
        return f"Order(id={self.id}, user_id={self.user_id}, status={self.status.value}, items={len(self._items)})"

    @property
    # Добавляем методы для работы с идентификатором заказа
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    # Добавляем методы для работы с идентификатором пользователя
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, value: int):
        self._user_id = value

    @property
    # Добавляем методы для работы со статусом заказа
    def status(self) -> OrderStatus:
        return self._status

    @status.setter
    def status(self, status: OrderStatus):
        if not isinstance(status, OrderStatus):
            raise TypeError("status must be OrderStatus enum")
        self._status = status


    @property
    # Добавляем методы для работы с платежным методом
    def payment_method(self) -> PaymentMethod | None:
        return self._payment_method


    @payment_method.setter
    def payment_method(self, payment_method: Optional[PaymentMethod]):
        if payment_method is not None and not isinstance(payment_method, PaymentMethod):
            raise TypeError("payment_method must be PaymentMethod enum or None")
        self._payment_method = payment_method


    @property
    # Добавляем методы для работы с датой создания заказа
    def created_at(self) -> datetime:
        return self._created_at


    def add_item(self, item: OrderItem):
        self._items.append(item)

    def del_item(self, item: OrderItem):
        pass