from typing import List, TYPE_CHECKING, Optional
from models.order_item import OrderItem
from utils.logger import setup_logger  # Добавить в импорты
logger = setup_logger(__name__)  # После всех импортов
logger.debug(f"Импортирован {__name__}")

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
        # Проверяем существование позиции
        existing = self._get_by_order_and_dish(order_id, dish.id)
        if existing:
            existing.quantity += quantity
            self._storage.save(existing)
        else:
            # Создаем новую позицию с правильными параметрами
            item = OrderItem(
                id=0,  # Временный ID (будет заменен при сохранении)
                order_id=order_id,
                dish=dish,
                quantity=quantity
            )
            saved_item = self._storage.save(item)
            assert saved_item.id > 0, "Позиция заказа не была сохранена"



    # В order_item_repo.py
    def update_quantity(self, item_id: int, quantity: int) -> None:
        logger.debug(f"Обновление количества: {item_id} -> {quantity}")
        item = self._storage.load_by_id(item_id)
        if not item:
            logger.error(f"Позиция {item_id} не найдена")
            raise ValueError("Позиция не найдена")
        item.quantity = quantity
        self._storage.save(item)

    def get_by_order(self, order_id: int) -> List['OrderItem']:
        """Возвращает все позиции в заказе."""
        return self._storage.get_by_order(order_id)  # Изменили load_by_order на get_by_order

    def get_by_id(self, item_id: int) -> Optional['OrderItem']:
        try:
            item = self._storage.load_by_id(item_id)
            if not item:
                logger.warning(f"Позиция {item_id} не найдена")
            return item
        except Exception as e:
            logger.error(f"Ошибка загрузки позиции {item_id}: {e}")
            return None


    def _get_by_order_and_dish(self, order_id: int, dish_id: int) -> Optional[OrderItem]:
        return self._storage.get_by_order_and_dish(order_id, dish_id)


    def delete_item(self, item_id: int) -> None:
        """Удаляет позицию из заказа"""
        self._storage.delete(item_id)

