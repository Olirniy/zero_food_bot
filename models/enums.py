# Изначальный enums
# from enum import Enum
#
# class OrderStatus(Enum):
#     IN_CART = "IN_CART"
#     PENDING = "PENDING"
#     PREPARING = "PREPARING"
#     DONE = "DONE"
#
# class PaymentMethod(Enum):
#     ONLINE = "ONLINE"
#     CASH = "CASH"



# models/enums.py (Расширенный enums)
from enum import Enum

class OrderStatus(Enum):
    IN_CART = "IN_CART"         # В корзине (не оформлен)
    PENDING = "PENDING"         # Ожидает подтверждения
    CONFIRMED = "CONFIRMED"     # Подтверждён рестораном
    PREPARING = "PREPARING"     # Готовится
    READY = "READY"             # Готов к выдаче
    ON_THE_WAY = "ON_THE_WAY"   # В пути (для доставки)
    DELIVERED = "DELIVERED"     # Доставлен
    CANCELLED = "CANCELLED"     # Отменён

class PaymentMethod(Enum):
    CASH = "CASH"               # Наличными при получении
    CARD = "CARD"               # Картой при получении
    ONLINE = "ONLINE" # Онлайн оплата картой
    ONLINE_WALLET = "ONLINE_WALLET" # Электронный кошелёк



class PaymentStatus(Enum):  # Добавляем новый enum
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"

