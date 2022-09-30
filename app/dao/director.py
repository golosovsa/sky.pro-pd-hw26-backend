"""
    DAO abstraction level
    Director DAO class
"""

from .base import BaseDAO
from .models import Director


class DirectorDAO(BaseDAO[Director]):
    __model__ = Director
    __updatable_fields__ = ["name", ]
