from typing import List
from models.payment import Payment, PaymentStatus

class PaymentRepository:
    def __init__(self, storage):
        self._storage = storage

    def create_payment(self, order_id: int, amount: float, method: str) -> Payment:
        payment = Payment(
            id=0,
            order_id=order_id,
            amount=amount,
            method=method,
            status=PaymentStatus.PENDING
        )
        return self._storage.save(payment)

    def get_order_payments(self, order_id: int) -> List[Payment]:
        return self._storage.load_by_order(order_id)

    def complete_payment(self, payment_id: int, transaction_id: str) -> Payment:
        payment = self._storage.load_by_id(payment_id)
        payment.status = PaymentStatus.COMPLETED
        payment.transaction_id = transaction_id
        return self._storage.save(payment)