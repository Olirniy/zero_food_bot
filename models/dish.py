from typing import Optional


class Dish:
    def __init__(self, id: int, category_id: int, name: str, short_description: str, description: str, price: float, photo_url: Optional[str]):
        self._id = id
        self._category_id = category_id
        self._name = name
        self._short_description = short_description
        self._description = description
        self._price = price
        self._photo_url = photo_url

    def __repr__(self) -> str:
        return f"Dish(id={self.id}, name='{self.name}', price={self.price}, category_id={self.category_id})"

    @property
    def id(self) -> int:
        return self._id

    @property
    def category_id(self) -> int:
        return self._category_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def short_description(self) -> str:
        return self._short_description

    @property
    def price(self) -> float:
        return self._price

    @property
    def photo_url(self) -> str | None:
        return self._photo_url