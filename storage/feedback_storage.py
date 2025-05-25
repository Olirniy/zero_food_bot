
from typing import List, Optional
from models.feedback import Feedback
import sqlite3
from datetime import datetime


def adapt_datetime(dt):
    return dt.isoformat()

def convert_datetime(ts):
    return datetime.fromisoformat(ts.decode())

sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("timestamp", convert_datetime)


class FeedbackStorage:
    def __init__(self, db_session: 'DBSession', sql_data: dict[str, str]) -> None:
        self._db_session = db_session
        self._sql_data = sql_data
        self._init_table()

    def _init_table(self) -> None:
        table_name = self._sql_data.get("tables", {}).get("feedback", "feedback")
        with self._db_session.get_session() as conn:
            conn.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    order_id INTEGER,
                    text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (order_id) REFERENCES orders(id)
                )
            ''')
            conn.commit()

    def save(self, feedback: Feedback) -> Feedback:
        with self._db_session.get_session() as conn:
            if feedback.id == 0:
                cursor = conn.execute(
                    f"INSERT INTO {self._sql_data['tables']['feedback']} "
                    "(user_id, order_id, text, created_at) VALUES (?, ?, ?, ?)",
                    (feedback.user_id,
                     feedback.order_id,
                     feedback.text,
                     feedback.created_at or datetime.now())  # Убедимся что есть дата
                )
                feedback._id = cursor.lastrowid
                # Получаем сохраненную запись, чтобы получить created_at из БД
                saved = self._load_by_id(conn, feedback.id)
                feedback._created_at = saved.created_at
            else:
                conn.execute(
                    f"UPDATE {self._sql_data['tables']['feedback']} SET "
                    "user_id=?, order_id=?, text=?, created_at=? WHERE id=?",
                    (feedback.user_id, feedback.order_id, feedback.text,
                     feedback.created_at, feedback.id)
                )
            conn.commit()
        return feedback

    def _load_by_id(self, conn, id: int) -> Optional[Feedback]:
        row = conn.execute(
            f"SELECT id, user_id, order_id, text, created_at "
            f"FROM {self._sql_data['tables']['feedback']} "
            "WHERE id = ?", (id,)
        ).fetchone()
        if not row:
            return None
        return Feedback(
            id=row[0],
            user_id=row[1],
            order_id=row[2],
            text=row[3],
            created_at=row[4]  # Уже datetime, не нужно преобразовывать
        )

    def load_all(self) -> List[Feedback]:
        return self.load_latest(1000)  # Практически все записи
