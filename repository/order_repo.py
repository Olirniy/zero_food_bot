
from datetime import datetime
from typing import Optional, List

from repository.order_item_repo import OrderItemRepository
from storage.order_storage import OrderStorage
from models.enums import OrderStatus
from models.order import Order


class OrderRepository:
    def __init__(self, storage: 'OrderStorage', item_repo: OrderItemRepository) -> None:
        self._storage = storage
        self._item_repo = item_repo
        self._orders: List['Order'] = storage.load_all()
        for order in self._orders:
            order.items = self._item_repo.get_by_order(order.id)

    def __get_new_id(self):
        if len(self._orders) == 0:
            return 1
        return max([order.id for order in self._orders])+1

    def get_in_cart(self, user_id: int) -> Optional[Order]:
        # Возвращает незавершённый заказ (IN_CART) для пользователя или None, если такого нет
        for order in self._orders:
            if order.user_id == user_id and order.status == OrderStatus.IN_CART:
                return order
        return None

    def get_by_id(self, order_id: int) -> Optional[Order]:
        for order in self._orders:
            if order.id == order_id:
                return order
        return None

    def create(self, user_id: int) -> 'Order':
        order = Order(id=self.__get_new_id(), user_id=user_id, status=OrderStatus.IN_CART, created_at=datetime.now(), payment_method=None)
        self.save(order)
        return order

    def save(self, order: Order) -> None:
        # Сохраняет новый или обновлённый заказ в памяти и в хранилище
        existing = next((o for o in self._orders if o.id == order.id), None)
        if existing is None:
            self._orders.append(order)
        else:
            idx = self._orders.index(existing)
            self._orders[idx] = order
        self._storage.save(order)

    def get_all_by_user(self, user_id: int) -> List[Order]:
        # Возвращает все заказы, созданные данным пользователем
        return [order for order in self._orders if order.user_id == user_id]

    def get_orders_by_status(self, status: OrderStatus) -> List[Order]:
        return [order for order in self._orders if order.status == status]

