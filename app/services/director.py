"""
    Service abstraction level
    Director service class
"""

from .base import BaseService
from app.dao import DirectorDAO


class DirectorService(BaseService[DirectorDAO]):
    def __init__(self, dao: DirectorDAO):
        self._dao = dao
