import pytest
from models.enums import OrderStatus, PaymentMethod
from storage.order_storage import OrderStorage
from config import SQL_DATA

@pytest.mark.parametrize("status, payment_method", [
    (OrderStatus.IN_CART, None),
    (OrderStatus.PENDING, PaymentMethod.CASH),
    (OrderStatus.CONFIRMED, PaymentMethod.ONLINE),
    (OrderStatus.PREPARING, None),
    (OrderStatus.DELIVERED, PaymentMethod.CARD),
    (OrderStatus.CANCELLED, None)
])
def test_order_statuses(db, sample_order, status, payment_method):
    storage = OrderStorage(db, SQL_DATA)

    # Обновляем заказ
    sample_order.status = status
    sample_order.payment_method = payment_method
    storage.save(sample_order)

    # Проверяем
    loaded = storage.load_by_id(sample_order.id)
    assert loaded.status == status
    assert loaded.payment_method == payment_method