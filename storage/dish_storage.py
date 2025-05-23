from typing import List, Optional, TYPE_CHECKING
from models.dish import Dish

if TYPE_CHECKING:
    from storage.db_session import DBSession

class DishStorage:
    def __init__(self, db_session: 'DBSession', sql_data: dict[str, str]) -> None:
        self._db_session = db_session
        self._sql_data = sql_data
        self._init_table()

    def _init_table(self) -> None:
        with self._db_session.get_session() as conn:
            conn.execute(f'''
                CREATE TABLE IF NOT EXISTS {self._sql_data["tables"]["dishes"]} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    short_description TEXT,
                    description TEXT,
                    price REAL NOT NULL,
                    photo_url TEXT,
                    FOREIGN KEY (category_id) REFERENCES {self._sql_data["tables"]["categories"]}(id)
                )
            ''')
            conn.commit()

    def save(self, dish: 'Dish') -> None:
        with self._db_session.get_session() as conn:
            conn.execute(
                f'''
                INSERT OR REPLACE INTO {self._sql_data["tables"]["dishes"]} 
                (id, category_id, name, short_description, description, price, photo_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (dish.id, dish.category_id, dish.name, dish.short_description,
                 dish.description, dish.price, dish.photo_url)
            )
            conn.commit()

    def load_by_id(self, dish_id: int) -> Optional['Dish']:
        with self._db_session.get_session() as conn:
            row = conn.execute(
                f"SELECT * FROM {self._sql_data['tables']['dishes']} WHERE id = ?",
                (dish_id,)
            ).fetchone()
            if not row:
                return None
            return Dish(
                id=row[0],
                category_id=row[1],
                name=row[2],
                short_description=row[3],
                description=row[4],
                price=row[5],
                photo_url=row[6]
            )

    def load_by_category(self, category_id: int) -> List['Dish']:
        with self._db_session.get_session() as conn:
            rows = conn.execute(
                f"SELECT * FROM {self._sql_data['tables']['dishes']} WHERE category_id = ?",
                (category_id,)
            ).fetchall()
            return [
                Dish(
                    id=row[0],
                    category_id=row[1],
                    name=row[2],
                    short_description=row[3],
                    description=row[4],
                    price=row[5],
                    photo_url=row[6]
                ) for row in rows
            ]