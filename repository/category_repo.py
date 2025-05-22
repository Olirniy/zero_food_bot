from sqlalchemy.orm import Session
from models.category import Category

def get_category_by_id(db: Session, category_id: int) -> Category:
    return db.query(Category).filter(Category.id == category_id).first()

def get_all_categories(db: Session) -> list[Category]:
    return db.query(Category).all()


def create_category(db: Session, name: str, description: str = None) -> Category:
    # Проверяем, существует ли категория с таким именем
    existing_category = db.query(Category).filter(Category.name == name).first()
    if existing_category:
        raise ValueError(f"Категория '{name}' уже существует")

    db_category = Category(name=name, description=description)
    db.add(db_category)
    try:
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        db.rollback()
        raise ValueError(f"Ошибка при создании категории: {str(e)}")