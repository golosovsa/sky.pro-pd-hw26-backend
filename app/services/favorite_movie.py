"""
    Service abstraction level
    Movie service class
"""
from typing import Optional, Tuple

from .base import BaseService
from app.dao import FavouriteMovieDAO
from ..dao.models import FavouriteMovies
from ..exceptions import ItemNotFound


class FavouriteMovieService(BaseService[FavouriteMovieDAO]):
    def __init__(self, dao: FavouriteMovieDAO):
        self._dao = dao

    def get_all_by_user_id(self, user_id: int, page: Optional[int] = None) -> Optional[FavouriteMovies]:
        return self._dao.get_all_by_user_id(user_id=user_id, page=page)

    def get_all_by_movie_id(self, movie_id: int, page: Optional[int] = None) -> Optional[FavouriteMovies]:
        return self._dao.get_all_by_movie_id(movie_id=movie_id, page=page)
