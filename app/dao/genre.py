"""
    DAO abstraction level
    Genre DAO class
"""

from .base import BaseDAO
from .models import Genre


class GenreDAO(BaseDAO[Genre]):
    __model__ = Genre
    __updatable_fields__ = ["name"]
