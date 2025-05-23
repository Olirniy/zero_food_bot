# repository/category_repo.py
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.category import Category
    from storage.category_storage import CategoryStorage

class CategoryRepository:
    def __init__(self, storage: 'CategoryStorage') -> None:
        self._storage = storage

    def get_all(self) -> List['Category']:
        return self._storage.load_all()

    def get_by_id(self, id: int) -> Optional['Category']:
        return self._storage.load_by_id(id)

    def create(self, category: 'Category') -> None:
        self._storage.save(category)

    def delete_all(self) -> None:
        # Реализация будет зависеть от метода в storage
        pass