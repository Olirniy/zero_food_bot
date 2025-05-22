from sqlalchemy.orm import Session
from storage.db import SessionLocal
from repository.category_repo import get_all_categories as repo_get_all_categories, create_category
from models.category import Category

def add_category(name: str, description: str = None):
    """Добавление новой категории"""
    with SessionLocal() as session:
        create_category(session, name, description)

def get_categories() -> list[Category]:
    """Получение всех категорий (алиас для совместимости)"""
    return get_all_categories()

def get_all_categories() -> list[Category]:
    """Основная функция получения категорий"""
    with SessionLocal() as session:
        return session.query(Category).all()

