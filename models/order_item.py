from models.dish import Dish


class OrderItem:
    def __init__(self, id: int, order_id: int, dish: Dish, quantity: int):
        self._id = id
        self._order_id = order_id
        self._dish = dish
        self._quantity = quantity

    @property
    def id(self) -> int:
        return self._id

    @property
    def order_id(self) -> int:
        return self._order_id

    @property
    def dish(self) -> Dish:
        return self._dish

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, quantity: int):
        self._quantity = quantity

    def get_item_sum(self) -> float:
        return self.dish.price * self.quantity