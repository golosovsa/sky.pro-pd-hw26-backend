"""
    Service abstraction level
    Movie service class
"""
from typing import Optional, List

from .base import BaseService
from app.exceptions import BadRequestData
from app.dao import MovieDAO
from ..setup.db import Base


class MovieService(BaseService[MovieDAO]):
    def __init__(self, dao: MovieDAO):
        super(MovieService, self).__init__(dao)
        self._dao = dao

    def get_all(self, page: Optional[int] = None, status: Optional[str] = None) -> List[Base]:
        if status is None:
            return super(MovieService, self).get_all(page=page)
        if isinstance(status, str) and status.lower() == "new":
            return self._dao.get_all_and_order_by_newest(page=page)
        raise BadRequestData()
