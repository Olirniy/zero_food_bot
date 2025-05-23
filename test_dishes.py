import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from storage.db_session import DBSession
from storage.dish_storage import DishStorage
from repository.dish_repo import DishRepository
from models.dish import Dish
from config import SQL_DATA


def test_dish_operations():
    # Инициализация
    db = DBSession()
    storage = DishStorage(db, SQL_DATA)
    repo = DishRepository(storage)

    # Тестовые данные
    test_dish = Dish(
        id=0,  # 0 для автоинкремента
        category_id=1,
        name="Тестовая пицца",
        short_description="Вкуснятина",
        description="Вкусная тестовая пицца",
        price=9.99,
        photo_url="test.jpg"
    )

    # Тестирование
    print("\n=== Тестирование работы с блюдами ===")

    # Создание
    created_dish = repo.create(test_dish)
    print(f"Создано блюдо: ID={created_dish.id}, Название={created_dish.name}")

    # Получение по ID
    loaded_dish = repo.get_by_id(created_dish.id)
    print(f"Загружено блюдо по ID: {loaded_dish.name if loaded_dish else 'Не найдено'}")

    # Получение по категории
    category_dishes = repo.get_by_category(1)
    print(f"Блюд в категории 1: {len(category_dishes)}")

    # Массовое добавление
    bulk_dishes = [
        Dish(0, 1, "Пепперони", "Острая пицца", "Новая", 45.00,"pepperoni.jpg"),
        Dish(0, 1, "Маргарита", "Классическая", "Прежняя", 87.00,"margarita.jpg")
    ]
    repo.create_bulk(bulk_dishes)
    print(f"Добавлено {len(bulk_dishes)} блюд массово")

    # Проверка результатов
    final_count = len(repo.get_by_category(1))
    print(f"Итого блюд в категории 1: {final_count}")
    print("=== Тест завершен ===")


if __name__ == "__main__":
    test_dish_operations()