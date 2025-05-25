from typing import Optional, TYPE_CHECKING
from models.user import User

if TYPE_CHECKING:
    from storage.db_session import DBSession

class UserStorage:
    def __init__(self, db_session: 'DBSession', sql_data: dict[str, str]):
        self._db = db_session
        self._table = sql_data["tables"]["users"]

    def save(self, user: 'User') -> 'User':  # Изменен тип возврата
        conn = self._db.get_session()
        try:
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
            return user  # Возвращаем сохраненного пользователя
        except Exception as e:
            conn.rollback()
            raise

    def load_by_telegram_id(self, telegram_id: int) -> Optional['User']:
        conn = self._db.get_session()
        row = conn.execute(
            f"SELECT id, telegram_id, username FROM {self._table} WHERE telegram_id = ?",
            (telegram_id,)
        ).fetchone()
        return User(*row) if row else None



