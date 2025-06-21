from typing import List, TYPE_CHECKING, Optional
from models.order_item import OrderItem  # Явный импорт
from models.dish import Dish  # Явный импорт
from utils.logger import setup_logger  # Добавить в импорты
logger = setup_logger(__name__)  # После всех импортов
logger.debug(f"Импортирован {__name__}")

if TYPE_CHECKING:
    from storage.db_session import DBSession


class OrderItemStorage:
    """Содержит методы для работы с позициями заказа"""

    def __init__(self, db_session: 'DBSession', sql_data: dict[str, str]) -> None:
        """Инициализирует хранилище позиций заказа"""
        self._db_session = db_session
        self._sql_data = sql_data
        self._init_table()

    def _init_table(self) -> None:
        """Инициализирует таблицу позиций заказа в базе данных"""
        with self._db_session.get_session() as conn:
            conn.execute(f'''
                CREATE TABLE IF NOT EXISTS {self._sql_data["tables"]["order_items"]} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    dish_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(id),
                    FOREIGN KEY (dish_id) REFERENCES dishes(id)
                )
            ''')
            conn.commit()

    def save(self, item: OrderItem) -> OrderItem:
        if item.dish.id == 0:
            raise ValueError("Блюдо должно быть сохранено в БД перед добавлением в заказ")

        with self._db_session.get_session() as conn:
            if item.id == 0:  # Новая позиция
                cursor = conn.execute(
                    f"INSERT INTO {self._sql_data['tables']['order_items']} "
                    "(order_id, dish_id, quantity) VALUES (?, ?, ?)",
                    (item.order_id, item.dish.id, item.quantity)
                )
                item._id = cursor.lastrowid
                logger.info(f"Создана позиция: ID={item.id}, order={item.order_id}, dish={item.dish.id}, qty={item.quantity}")
            else:  # Обновление
                conn.execute(
                    f"UPDATE {self._sql_data['tables']['order_items']} "
                    "SET quantity=? WHERE id=?",
                    (item.quantity, item.id)
                )
                logger.info(f"Обновлена позиция: ID={item.id}, qty={item.quantity}")
            conn.commit()
        return item

    def get_by_order(self, order_id: int) -> List['OrderItem']:
        """Возвращает список позиций заказа по ID заказа"""
        with self._db_session.get_session() as conn:
            # Запрос с использованием JOIN и таблицы блюд
            rows = conn.execute(
                f'''
                SELECT oi.id, oi.order_id, oi.dish_id, oi.quantity,
                       d.id, d.category_id, d.name, d.short_description, 
                       d.description, d.price, d.photo_url
                FROM {self._sql_data["tables"]["order_items"]} oi
                JOIN {self._sql_data["tables"]["dishes"]} d ON oi.dish_id = d.id
                WHERE oi.order_id = ?
                ''',
                (order_id,)
            ).fetchall()

            return [
                OrderItem(
                    id=row[0],
                    order_id=row[1],
                    dish=Dish(
                        id=row[4], category_id=row[5], name=row[6],
                        short_description=row[7], description=row[8],
                        price=row[9], photo_url=row[10]
                    ),
                    quantity=row[3]
                ) for row in rows
            ]

    def load_by_id(self, item_id: int) -> Optional['OrderItem']:
        with self._db_session.get_session() as conn:
            row = conn.execute(
                f'''
            SELECT oi.id, oi.order_id, oi.dish_id, oi.quantity,
                   d.id, d.category_id, d.name, d.short_description, 
                   d.description, d.price, d.photo_url
            FROM {self._sql_data["tables"]["order_items"]} oi
            JOIN {self._sql_data["tables"]["dishes"]} d ON oi.dish_id = d.id
            WHERE oi.id = ?
            ''',
                (item_id,)
            ).fetchone()
            # ... остальной код
            if not row:
                return None

            return OrderItem(
                id=row[0],
                order_id=row[1],
                dish=Dish(
                    id=row[4], category_id=row[5], name=row[6],
                    short_description=row[7], description=row[8],
                    price=row[9], photo_url=row[10]
                ),
                quantity=row[3]
            )

    def delete(self, item_id: int) -> None:
        with self._db_session.get_session() as conn:
            conn.execute(
                f"DELETE FROM {self._sql_data['tables']['order_items']} WHERE id = ?",
                (item_id,)
            )
            conn.commit()


    # В класс OrderItemStorage добавим:
    def get_by_order_and_dish(self, order_id: int, dish_id: int) -> Optional['OrderItem']:
        with self._db_session.get_session() as conn:
            row = conn.execute(
                f'''
                SELECT oi.id, oi.order_id, oi.dish_id, oi.quantity,
                       d.id, d.category_id, d.name, d.short_description, 
                       d.description, d.price, d.photo_url
                FROM {self._sql_data["tables"]["order_items"]} oi
                JOIN {self._sql_data["tables"]["dishes"]} d ON oi.dish_id = d.id
                WHERE oi.order_id = ? AND oi.dish_id = ?
                ''',
                (order_id, dish_id)
            ).fetchone()

            if not row:
                return None

            return OrderItem(
                id=row[0],
                order_id=row[1],
                dish=Dish(
                    id=row[4], category_id=row[5], name=row[6],
                    short_description=row[7], description=row[8],
                    price=row[9], photo_url=row[10]
                ),
                quantity=row[3]
            )