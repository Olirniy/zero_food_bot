
from typing import List

from storage.order_items_storage import OrderItemStorage
from models.order_item import OrderItem


class OrderItemRepository:
    def __init__(self, storage: 'OrderItemStorage') -> None:
        self._storage: 'OrderItemStorage' = storage
        self._repository: List['OrderItem'] = storage.load_all()

    def __get_new_id(self) -> int:
        return max((item.id for item in self._repository), default=0) + 1

    def new_item(self, order_id: int, dish_id: int, dish_name: str, dish_price: float, quantity: int) -> 'OrderItem':
        new_id: int = self.__get_new_id()
        new_item: OrderItem = OrderItem(id=new_id, order_id=order_id, dish_id=dish_id, quantity=quantity, dish_name=dish_name, dish_price=dish_price)
        self._repository.append(new_item)
        self._storage.save(new_item)
        return new_item

    def update_quantity(self, item_id: int, quantity: int) -> None:
        for item in self._repository:
            if item.id == item_id:
                item.quantity = quantity
                self._storage.save(item)
                return

    def get_by_order(self, order_id: int) -> List['OrderItem']:
        return [item for item in self._repository if item.order_id == order_id]

    def delete_item(self, item_id: int) -> None:
        for index, item in enumerate(self._repository):
            if item.id == item_id:
                del self._repository[index]
                self._storage.delete(item_id)
                return

