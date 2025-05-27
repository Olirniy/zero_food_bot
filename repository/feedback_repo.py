
from datetime import datetime
from typing import List, TYPE_CHECKING, Optional


from models.feedback import Feedback
from storage.feedback_storage import FeedbackStorage

class FeedbackRepository:
    def __init__(self, storage: 'FeedbackStorage'):
        self._storage = storage
        self._repository:list['Feedback'] = storage.load_all()

    def _get_new_feedback_id(self) -> int:
        if not self._repository:
            return 1
        return max(feedback.id for feedback in self._repository) + 1

    def new_feedback(self, user_id: int, user_name: str, text: str, order_id: Optional[int] = None) -> 'Feedback':
        id=self._get_new_feedback_id()
        feedback = Feedback(id, user_id, user_name, order_id, text, datetime.now())
        self._repository.append(feedback)
        self._storage.save(feedback)
        return feedback

    def add_existing(self, feedback: 'Feedback') -> None:
        self._repository.append(feedback)

    def get_latest(self, n: int) -> List['Feedback']:
        pass

    def get_all(self) -> List['Feedback']:
        return self._repository

