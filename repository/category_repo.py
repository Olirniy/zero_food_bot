from sqlalchemy.orm import Session
from models.category import Category

def create_category(db: Session, name: str, description: str = None) -> Category:
    """Создание категории в репозитории"""
    db_category = Category(name=name, description=description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_all_categories(db: Session) -> list[Category]:
    """Получение всех категорий из репозитория"""
    return db.query(Category).all()

