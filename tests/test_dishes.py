import pytest
from storage.dish_storage import DishStorage
from repository.dish_repo import DishRepository
from models.dish import Dish
from config import SQL_DATA

def test_dish_operations(db):
    storage = DishStorage(db, SQL_DATA)
    repo = DishRepository(storage)

    # Тест создания
    test_dish = Dish(
        id=0,
        category_id=1,
        name="Тестовая пицца",
        short_description="Вкуснятина",
        description="Вкусная тестовая пицца",
        price=9.99,
        photo_url="test.jpg"
    )
    created_dish = repo.create(test_dish)
    assert created_dish is not None
    assert created_dish.id > 0
    assert created_dish.name == test_dish.name

def test_bulk_operations(db):
    storage = DishStorage(db, SQL_DATA)
    repo = DishRepository(storage)

    # Создаем тестовые блюда
    dish1 = Dish(
        id=0, category_id=1, name="Пепперони",
        short_description="Острая", description="",
        price=45.00, photo_url="test.jpg"
    )
    dish2 = Dish(
        id=0, category_id=1, name="Маргарита",
        short_description="Классика", description="",
        price=87.00, photo_url="test.jpg"
    )

    repo.create_bulk([dish1, dish2])
    items = repo.get_by_category(1)
    assert len(items) >= 2

@pytest.mark.parametrize("dish_data", [
    {
        "name": "Пепперони",
        "price": 12.99,
        "category_id": 1,
        "short_description": "Острая пицца",
        "description": "С пепперони и перцем"
    },
    {
        "name": "Маргарита",
        "price": 10.99,
        "category_id": 1,
        "short_description": "Классическая",
        "description": "С моцареллой и томатами"
    },
    {
        "name": "Веган",
        "price": 9.99,
        "category_id": 2,
        "short_description": "Растительная",
        "description": "С овощами и тофу"
    }
])
def test_dish_variations(db, dish_data):
    storage = DishStorage(db, SQL_DATA)
    dish = Dish(
        id=0,
        category_id=dish_data["category_id"],
        name=dish_data["name"],
        short_description=dish_data["short_description"],
        description=dish_data["description"],
        price=dish_data["price"],
        photo_url="test.jpg"
    )
    created = storage.save(dish)
    assert created.id > 0
    assert created.name == dish.name