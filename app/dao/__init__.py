from .base import BaseDAO
from .director import DirectorDAO
from .genre import GenreDAO
from .user import UserDAO
from .movie import MovieDAO
from .favourite_movie import FavouriteMovieDAO

__all__ = [
    "BaseDAO",
    "DirectorDAO",
    "GenreDAO",
    "UserDAO",
    "MovieDAO",
    "FavouriteMovieDAO",
]
