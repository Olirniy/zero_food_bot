class Category:
    def __init__(self, id: int, name: str):
        self._id = id
        self._name = name

    def __repr__(self) -> str:
        return f"Category(id={self.id}, name='{self.name}')"

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name