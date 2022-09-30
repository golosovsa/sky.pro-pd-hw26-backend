"""
    Users SQLAlchemy model
"""

from sqlalchemy import Column, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from app.setup.db.models import BaseWithID, KeyType


class User(BaseWithID):
    __tablename__ = 'users'

    email = Column(String(100), unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String(40))
    surname = Column(String(40))
    favourite_genre = Column(KeyType, ForeignKey("genres.id"))
    # many to one
    favourite_genre_object = relationship("Genre", lazy="noload")
    # maby to many
    favourite_movies = relationship("Movie", secondary="favorite_movies", lazy="noload")

