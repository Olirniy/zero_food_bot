from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from storage.order_storage import OrderStorage
    from models.enums import OrderStatus
    from models.order import Order


class OrderRepository:
    def __init__(self, storage: 'OrderStorage') -> None:
        self._storage = storage

    def get_in_cart(self, user_id: int) -> Optional['Order']:
        """Возвращает активный заказ (корзину) пользователя."""
        orders = self._storage.load_by_user(user_id)
        for order in orders:
            if order.status == OrderStatus.IN_CART:
                return order
        return None

    def create(self, user_id: int) -> 'Order':
        """Создает новый заказ (корзину) для пользователя."""
        from models.enums import OrderStatus
        order = Order(
            id=0,
            user_id=user_id,
            status=OrderStatus.IN_CART,
            payment_method=None,
            created_at=None
        )
        self._storage.save(order)
        return order

    def update_status(self, order_id: int, status: 'OrderStatus') -> None:
        """Обновляет статус заказа (например, "Оплачен")."""
        order = self._storage.load_by_id(order_id)
        if not order:
            raise ValueError("Заказ не найден")
        order.status = status
        self._storage.save(order)

    def get_all_by_user(self, user_id: int) -> List['Order']:
        """Возвращает все заказы пользователя."""
        return self._storage.load_by_user(user_id)