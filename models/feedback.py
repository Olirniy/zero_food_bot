
from datetime import datetime
from typing import Optional


class Feedback:
    def __init__(self, id: int, user_id: int, user_name: str, order_id: Optional[int], text: str, created_at: datetime):
        self._id = id
        self._user_id = user_id
        self._user_name = user_name
        self._order_id = order_id
        self._text = text
        self._created_at = created_at

    @property
    def id(self) -> int:
        return self._id

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def user_name(self) -> str:
        return self._user_name

    @property
    def order_id(self) -> Optional[int]:
        return self._order_id

    @property
    def text(self) -> str:
        return self._text

    @property
    def created_at(self) -> datetime:
        return self._created_at

