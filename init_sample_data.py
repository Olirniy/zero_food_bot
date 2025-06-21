from storage.db_session import DBSession
from models.category import Category
from models.dish import Dish
from storage.category_storage import CategoryStorage
from storage.dish_storage import DishStorage
from config import SQL_DATA
import os

def init_sample_data():
    # Удаляем старую БД, если существует
    db_path = SQL_DATA['db_path']
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗑 Удалена старая БД: {db_path}")

    db = DBSession()

    # Инициализация хранилищ
    category_storage = CategoryStorage(db, SQL_DATA)
    dish_storage = DishStorage(db, SQL_DATA)

    # Создаем категории
    categories = [
        Category(id=0, name="🍕 Пицца"),
        Category(id=0, name="🍔 Бургеры"),
        Category(id=0, name="🥤 Напитки"),
        Category(id=0, name="🥗 Салаты"),
        Category(id=0, name="🍰 Десерты")
    ]

    # Сохраняем категории и получаем их реальные ID
    saved_categories = []
    for category in categories:
        category_storage.save(category)
        # Для надежности перезагружаем категорию из БД
        last_category = category_storage.load_all()[-1]
        saved_categories.append(last_category)
        print(f"✅ Создана категория: {last_category.name} (ID: {last_category.id})")

    # Создаем блюда с ПРАВИЛЬНЫМИ category_id
    dishes = [
        # Пиццы
        Dish(0, saved_categories[0].id, "Маргарита", "Классическая", "Тесто, томаты, сыр моцарелла, базилик", 450.0, None),
        Dish(0, saved_categories[0].id, "Пепперони", "Острая", "Тесто, томатный соус, пепперони, сыр", 550.0, None),
        Dish(0, saved_categories[0].id, "4 Сыра", "Сырное ассорти", "Моцарелла, горгонзола, пармезан, фонтина", 600.0, None),

        # Бургеры
        Dish(0, saved_categories[1].id, "Чизбургер", "С говядиной", "Булочка, котлета, сыр, салат, соус", 350.0, None),
        Dish(0, saved_categories[1].id, "Чикенбургер", "С курицей", "Булочка, куриная котлета, салат, соус", 320.0, None),
        Dish(0, saved_categories[1].id, "Вегетарианский", "С овощами", "Булочка, овощная котлета, помидоры, салат", 400.0, None),

        # Напитки
        Dish(0, saved_categories[2].id, "Кола", "Освежающий", "0.5л", 150.0, None),
        Dish(0, saved_categories[2].id, "Лимонад", "Домашний", "0.5л, свежий, с мятой", 180.0, None),
        Dish(0, saved_categories[2].id, "Сок апельсиновый", "Свежевыжатый", "0.3л", 200.0, None),

        # Десерты
        Dish(0, saved_categories[4].id, "Чизкейк", "Нью-Йоркский", "Нежный творожный десерт", 350.0, None),
        Dish(0, saved_categories[4].id, "Тирамису", "Классический", "Печенье савоярди, кофе, сыр маскарпоне", 380.0, None)
    ]

    # Сохраняем блюда
    for dish in dishes:
        dish_storage.save(dish)
        print(f"🍽 Добавлено блюдо: {dish.name} в категорию ID: {dish.category_id}")

    print("✅ Все тестовые данные успешно добавлены!")

if __name__ == "__main__":
    init_sample_data()