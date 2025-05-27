
from enum import Enum

class OrderStatus(Enum):
    IN_CART = "IN_CART"
    PENDING = "PENDING"
    PREPARING = "PREPARING"
    DONE = "DONE"
    def get_name(self):
        if self == OrderStatus.IN_CART: return "В корзине"
        if self == OrderStatus.PENDING: return "В обработке"
        if self == OrderStatus.PREPARING: return "Готовится"
        if self == OrderStatus.DONE: return "Выдан"

class PaymentMethod(Enum):
    ONLINE = "ONLINE"
    CASH = "CASH"
    def get_name(self):
        if self == PaymentMethod.ONLINE: return "Карта"
        if self == PaymentMethod.CASH: return "Наличные"

