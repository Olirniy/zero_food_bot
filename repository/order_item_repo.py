from typing import List, TYPE_CHECKING
from models.order_item import OrderItem

if TYPE_CHECKING:
    from storage.order_items_storage import OrderItemStorage
    from models.order_item import OrderItem
    from models.dish import Dish


class OrderItemRepository:
    def __init__(self, storage: 'OrderItemStorage') -> None:
        self._storage = storage

    # repository/order_item_repo.py
    def add_item(self, order_id: int, dish: 'Dish', quantity: int) -> None:
        """Добавляет блюдо в заказ с указанным количеством"""
        item = OrderItem(
            id=0,
            order_id=order_id,
            dish=dish,
            quantity=quantity
        )
        saved_item = self._storage.save(item)  # Сохраняем и получаем результат
        assert saved_item.id > 0, "Позиция заказа не была сохранена"

    def update_quantity(self, item_id: int, quantity: int) -> None:
        """Изменяет количество блюда в заказе."""
        items = self._storage.load_by_order(item_id)
        if not items:
            raise ValueError("Позиция не найдена")
        item = items[0]
        item.quantity = quantity
        self._storage.save(item)

    def get_by_order(self, order_id: int) -> List['OrderItem']:
        """Возвращает все позиции в заказе."""
        return self._storage.get_by_order(order_id)  # Изменили load_by_order на get_by_order

    def delete_item(self, item_id: int) -> None:
        """Удаляет позицию из заказа."""
        # Реализация зависит от метода в storage (можно добавить delete_by_id)
        raise NotImplementedError("Метод пока не реализован")