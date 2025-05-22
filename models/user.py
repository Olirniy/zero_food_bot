from sqlalchemy import Column, Integer, String
from storage.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(50))
    first_name = Column(String(50))

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id})>"

    # @property
    # def id(self) -> int:
    #     return self._id
    #
    # @property
    # def telegram_id(self) -> int:
    #     return self._telegram_id
    #
    # @property
    # def username(self) -> str:
    #     return self._username
    #
    # @property
    # def first_name(self) -> str:
    #     return self._first_name