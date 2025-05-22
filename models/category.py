# # models/category.py
#
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship
# from storage.db import Base
#
#
# class Category(Base):
#     __tablename__ = 'categories'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), unique=True, nullable=False)
#     description = Column(String(255))
#
#     # Обратная связь с блюдами
#     dishes = relationship("Dish", back_populates="category")

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from storage.db import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))

    # Ленивая загрузка связи
    dishes = relationship("Dish", back_populates="category", lazy='dynamic')