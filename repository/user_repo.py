# repository/user_repo.py
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from storage.user_storage import UserStorage
    from models.user import User

class UserRepository:
    def __init__(self, storage: 'UserStorage') -> None:
        self._storage = storage

    def get_or_create(self, telegram_id: int, username: str) -> 'User':
        user = self._storage.load_by_telegram_id(telegram_id)
        if not user:
            user = User(id=0, telegram_id=telegram_id, username=username)
            self._storage.save(user)
            user = self._storage.load_by_telegram_id(telegram_id)
        return user

    def get_by_telegram_id(self, telegram_id: int) -> Optional['User']:
        return self._storage.load_by_telegram_id(telegram_id)







#
#
# class UserRepository:
#     def __init__(self, storage: 'UserStorage') -> None:
#         self._storage: 'UserStorage' = storage
#
#     def get_or_create(self, telegram_id: int, username: str) -> 'User':
#         pass
#
#     def get_by_telegram_id(self, telegram_id: int) -> Optional['User']:
#         pass
