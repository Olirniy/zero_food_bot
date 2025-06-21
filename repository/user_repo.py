from typing import Optional, TYPE_CHECKING
from models.user import User

if TYPE_CHECKING:
    from storage.user_storage import UserStorage

class UserRepository:
    def __init__(self, storage: 'UserStorage'):
        self._storage = storage

    def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        return self._storage.load_by_telegram_id(telegram_id)

    def create(self, telegram_id: int, username: str) -> User:
        """Создает пользователя и возвращает объект с ID"""
        new_user = User(id=0, telegram_id=telegram_id, username=username)
        saved_user = self._storage.save(new_user)
        if not saved_user.id:
            raise ValueError("Не удалось создать пользователя")
        return saved_user

    def get_or_create(self, telegram_id: int, username: str) -> User:
        """Получает или создает пользователя"""
        user = self.get_by_telegram_id(telegram_id)
        if not user:
            user = self.create(telegram_id, username)
        return user







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
