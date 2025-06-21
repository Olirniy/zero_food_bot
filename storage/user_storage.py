from typing import Optional, TYPE_CHECKING
from models.user import User
from utils.logger import setup_logger  # Добавить в импорты
logger = setup_logger(__name__)  # После всех импортов
logger.debug(f"Импортирован {__name__}")


if TYPE_CHECKING:
    from storage.db_session import DBSession




class UserStorage:
    def __init__(self, db_session, sql_data: dict):
        self._db = db_session
        self._table = sql_data["tables"]["users"]

    def save(self, user: User) -> User:
        """Сохраняет пользователя и возвращает его с обновленным ID"""
        with self._db.get_session() as conn:
            if user.id == 0:  # Новый пользователь
                cursor = conn.execute(
                    f"INSERT INTO {self._table} (telegram_id, username) VALUES (?, ?)",
                    (user.telegram_id, user.username)
                )
                user._id = cursor.lastrowid
            else:  # Обновление
                conn.execute(
                    f"UPDATE {self._table} SET username = ? WHERE id = ?",
                    (user.username, user.id)
                )
            conn.commit()
        return user

    def load_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        with self._db.get_session() as conn:
            row = conn.execute(
                f"SELECT id, telegram_id, username FROM {self._table} WHERE telegram_id = ?",
                (telegram_id,)
            ).fetchone()
            return User(*row) if row else None



