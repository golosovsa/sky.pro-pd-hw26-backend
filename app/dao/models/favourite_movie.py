"""
    FavoriteMovies SQLAlchemy model
"""

from sqlalchemy import Column, ForeignKey, BigInteger

from app.setup.db.models import BaseManyToMany, KeyType


class FavouriteMovies(BaseManyToMany):
    __tablename__ = "favorite_movies"

    user_id = Column(KeyType, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, autoincrement=False)
    movie_id = Column(KeyType, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True, autoincrement=False)

