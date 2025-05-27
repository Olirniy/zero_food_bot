
from typing import List, Optional
from datetime import datetime

from models.feedback import Feedback
from storage.db_session import DBSession

class FeedbackStorage:
    def __init__(self, db_session: DBSession, sql_data: dict[str, str]) -> None:
        """Инициализирует хранилище обратной связи, создаёт таблицу, если её нет."""
        self._db_session: DBSession = db_session
        self._sql_data: dict[str, str] = sql_data
        self._init_table()

    def _init_table(self) -> None:
        """Создаёт таблицу для хранения отзывов по имени из sql_data, если она не существует."""
        conn = self._db_session.get_session()
        cursor = conn.cursor()
        table_name: str = self._sql_data['feedback_table_name']
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                order_id INTEGER,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """
        )
        conn.commit()
        conn.close()

    def save(self, feedback: Feedback) -> None:
        """Сохраняет объект Feedback в базу данных. Если запись с таким id существует — обновляет её."""
        conn = self._db_session.get_session()
        cursor = conn.cursor()
        table_name: str = self._sql_data['feedback_table_name']
        cursor.execute(
            f"""
                INSERT OR REPLACE INTO {table_name} (
                    id, user_id, user_name, order_id, text, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                feedback.id,
                feedback.user_id,
                feedback.user_name,
                feedback.order_id,
                feedback.text,
                feedback.created_at.isoformat()
            )
        )
        conn.commit()
        conn.close()

    def load_latest(self, n: int) -> List[Feedback]:
        """Загружает последние n отзывов, отсортированных по дате создания по убыванию."""
        conn = self._db_session.get_session()
        cursor = conn.cursor()
        table_name: str = self._sql_data['feedback_table_name']
        cursor.execute(
            f"""
                SELECT id, user_id, user_name, order_id, text, created_at
                FROM {table_name}
                ORDER BY datetime(created_at) DESC
                LIMIT ?
            """,
            (n,)
        )
        rows = cursor.fetchall()
        feedbacks: List[Feedback] = []
        conn.close()
        for id_, user_id, user_name, order_id, text, created_at_str in rows:
            created_at: datetime = datetime.fromisoformat(created_at_str)
            feedbacks.append(Feedback(id_, user_id, user_name, order_id, text, created_at))
        return feedbacks

    def load_all(self) -> List[Feedback]:
        """Загружает все отзывы из базы данных."""
        conn = self._db_session.get_session()
        cursor = conn.cursor()
        table_name: str = self._sql_data['feedback_table_name']
        cursor.execute(
            f"""
                SELECT id, user_id, user_name, order_id, text, created_at
                FROM {table_name}
                ORDER BY datetime(created_at) DESC
            """
        )
        rows = cursor.fetchall()
        feedbacks: List[Feedback] = []
        conn.close()
        for id_, user_id, user_name, order_id, text, created_at_str in rows:
            created_at: datetime = datetime.fromisoformat(created_at_str)
            feedbacks.append(Feedback(id_, user_id, user_name, order_id, text, created_at))
        return feedbacks

