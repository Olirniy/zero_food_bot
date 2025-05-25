import pytest
from models.payment import PaymentStatus
from models.enums import OrderStatus
from config import SQL_DATA
from storage.payment_storage import PaymentStorage
from storage.db_session import DBSession
from models.enums import OrderStatus, PaymentStatus
from models.enums import PaymentStatus, OrderStatus


def test_payment_creation(payment_repo, sample_order):
    payment = payment_repo.create_payment(
        order_id=sample_order.id,
        amount=100.0,
        method="card"
    )
    assert payment.id > 0
    assert payment.status == PaymentStatus.PENDING


def test_order_payment_flow(order_storage, payment_repo, sample_order, order_item_repo):
    """Интеграционный тест полного цикла заказ->платеж"""
    # Создаем репозиторий с нужными зависимостями
    from repository.order_repo import OrderRepository
    order_repo = OrderRepository(order_storage, order_item_repo)

    # Обновляем статус заказа
    order = order_storage.load_by_id(sample_order.id)
    order.status = OrderStatus.PENDING
    order_storage.save(order)

    # Создаем платеж
    payment = payment_repo.create_payment(
        order_id=sample_order.id,
        amount=150.0,
        method="card"
    )

    # Проверяем результаты
    payments = payment_repo.get_order_payments(sample_order.id)
    assert len(payments) == 1
    assert payments[0].status == PaymentStatus.PENDING
    assert order.status == OrderStatus.PENDING