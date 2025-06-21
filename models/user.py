class User:
    def __init__(self, id: int, telegram_id: int, username: str):
        self._id = id
        self._telegram_id = telegram_id
        self._username = username

    def __repr__(self) -> str:
        return f"User(id={self.id}, tg_id={self.telegram_id}, username='{self.username}')"

    @property
    def id(self) -> int:
        return self._id

    @property
    def telegram_id(self) -> int:
        return self._telegram_id

    @property
    def username(self) -> str:
        return self._username