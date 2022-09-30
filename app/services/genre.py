"""
    Service abstraction level
    Genre service class
"""

from .base import BaseService
from app.dao import GenreDAO


class GenreService(BaseService[GenreDAO]):
    def __init__(self, dao: GenreDAO):
        self._dao = dao
