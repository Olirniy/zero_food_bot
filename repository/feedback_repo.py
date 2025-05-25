from typing import List
from models.feedback import Feedback

class FeedbackRepository:
    def __init__(self, storage: 'FeedbackStorage'):
        self._storage = storage

    def create(self, user_id: int, text: str, order_id: int = None) -> Feedback:
        feedback = Feedback(
            id=0,
            user_id=user_id,
            order_id=order_id,
            text=text,
            created_at=None  # Будет установлено в БД
        )
        return self._storage.save(feedback)

    def get_latest(self, n: int = 5) -> List[Feedback]:
        return self._storage.load_latest(n)