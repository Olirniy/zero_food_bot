from sqlalchemy.orm import Session
from storage.db import SessionLocal
from repository.category_repo import get_all_categories, create_category

def add_category(name: str, description: str = None):
    with SessionLocal() as session:
        create_category(session, name, description)

def get_categories() -> list:
    with SessionLocal() as session:
        return get_all_categories(session)

def get_categories():
    with SessionLocal() as session:
        return get_all_categories(session)

