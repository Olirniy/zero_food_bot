# storage/category_storage.py
from typing import Optional, List, TYPE_CHECKING
from models.category import Category

if TYPE_CHECKING:
    from storage.db_session import DBSession

class CategoryStorage:
    def __init__(self, db_session: 'DBSession', sql_data: dict[str, str]) -> None:
        self._db_session = db_session
        self._sql_data = sql_data
        self._init_table()

    def _init_table(self) -> None:
        with self._db_session.get_session() as conn:
            conn.execute(f'''
                CREATE TABLE IF NOT EXISTS {self._sql_data["tables"]["categories"]} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            ''')
            conn.commit()

    def save(self, category: 'Category') -> None:
        with self._db_session.get_session() as conn:
            conn.execute(
                f"INSERT OR REPLACE INTO {self._sql_data['tables']['categories']} (id, name) VALUES (?, ?)",
                (category.id, category.name)
            )
            conn.commit()

    def load_by_id(self, id: int) -> Optional['Category']:
        with self._db_session.get_session() as conn:
            row = conn.execute(
                f"SELECT id, name FROM {self._sql_data['tables']['categories']} WHERE id = ?", (id,)
            ).fetchone()
            return Category(*row) if row else None

    def load_all(self) -> List['Category']:
        with self._db_session.get_session() as conn:
            rows = conn.execute(f"SELECT id, name FROM {self._sql_data['tables']['categories']}").fetchall()
            return [Category(*row) for row in rows]