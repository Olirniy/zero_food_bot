
from typing import List, Optional, TYPE_CHECKING



if TYPE_CHECKING:
    from models.category import Category
    from storage.category_storage import CategoryStorage


class CategoryRepository:
    def __init__(self, storage: 'CategoryStorage') -> None:
        self._storage: 'CategoryStorage' = storage
        self._categories: List['Category'] = self._storage.load_all()

    def get_all(self) -> List['Category']:
        return self._categories

    def get_by_id(self, id: int) -> Optional['Category']:
        for category in self._categories:
            if category.id == id:
                return category
        return None

    def create(self, category: 'Category') -> None:
        self._categories.append(category)
        self._storage.save(category)

    def del_all(self) -> None:
        self._categories.clear()
        self._storage.del_all()

