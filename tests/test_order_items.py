import pytest
from storage.order_items_storage import OrderItemStorage
from repository.order_item_repo import OrderItemRepository
from config import SQL_DATA

def test_order_items_operations(db, sample_order, sample_dish):
    storage = OrderItemStorage(db, SQL_DATA)
    repo = OrderItemRepository(storage)

    # Добавление позиции заказа
    repo.add_item(sample_order.id, sample_dish, 2)

    # Проверка результатов
    items = repo.get_by_order(sample_order.id)
    assert len(items) == 1
    assert items[0].dish.id == sample_dish.id
    assert items[0].quantity == 2