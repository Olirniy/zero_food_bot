from storage.db_session import DBSession
from models.category import Category
from models.dish import Dish
from repository.category_repo import CategoryRepository
from repository.dish_repo import DishRepository
from config import SQL_DATA



def init_sample_data():
    db = DBSession()

    # Категории
    categories = [
        Category(id=0, name="Пицца"),
        Category(id=0, name="Суши"),
        Category(id=0, name="Напитки")
    ]

    # Блюда
    dishes = [
        # Пиццы
        Dish(0, categories[0].id, "Маргарита", "Классическая итальянская", "Тесто, томаты, сыр моцарелла, базилик", 450.0, None),
        Dish(0, categories[0].id, "Пепперони", "Острая с колбасками", "Тесто, томатный соус, пепперони, сыр", 550.0, None),

        # Бургеры
        Dish(0, categories[1].id, "Чизбургер", "С говяжьей котлетой", "Булочка, котлета, сыр, салат, соус", 350.0, None),
        Dish(0, categories[1].id, "Вегетарианский", "С овощной котлетой", "Булочка, овощная котлета, помидоры, салат", 400.0, None),

        # Напитки
        Dish(0, categories[2].id, "Кола", "Освежающий напиток", "0.5л", 150.0, None),
        Dish(0, categories[2].id, "Лимонад", "Домашний лимонад", "0.5л, свежий, с мятой", 180.0, None)
    ]

    # Сохранение
    category_repo = CategoryRepository(db)
    dish_repo = DishRepository(db)

    for cat in categories:
        category_repo.create(cat)

    dish_repo.create_bulk(dishes)

if __name__ == "__main__":
    init_sample_data()