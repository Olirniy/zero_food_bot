from typing import Optional, List, TYPE_CHECKING
from models.enums import OrderStatus

if TYPE_CHECKING:
    from storage.order_storage import OrderStorage
    from models.order import Order
    from repository.order_item_repo import OrderItemRepository






class OrderRepository:
    def __init__(self, storage: 'OrderStorage', order_item_repo: 'OrderItemRepository'):
        self._storage = storage
        self._order_item_repo = order_item_repo

    def get_in_cart(self, user_id: int) -> Optional['Order']:
        orders = self._storage.load_by_user(user_id)
        for order in orders:
            if order.status == OrderStatus.IN_CART:
                return order
        return None

    def create(self, user_id: int) -> 'Order':
        order = Order(
            id=0,
            user_id=user_id,
            status=OrderStatus.IN_CART,
            payment_method=None,
            created_at=None
        )
        return self._storage.save(order)

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

    def calculate_order_total(self, order_id: int) -> float:
        order_items = self._order_item_repo.get_by_order(order_id)
        return sum(item.dish.price * item.quantity for item in order_items)

    def get_user_cart(self, user_id: int) -> Optional['Order']:
        """Находит корзину пользователя (IN_CART)"""
        orders = self.get_all_by_user(user_id)
        return next((o for o in orders if o.status == OrderStatus.IN_CART), None)