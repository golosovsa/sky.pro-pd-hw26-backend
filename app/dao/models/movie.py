"""
    Movies SQLAlchemy model
"""

from sqlalchemy import Column, String, Text, Integer, Float, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from app.setup.db.models import BaseWithID, KeyType


class Movie(BaseWithID):
    __tablename__ = 'movies'

    title = Column(String(100), nullable=False)
    description = Column(Text)
    trailer = Column(String(100))
    year = Column(Integer)
    rating = Column(Float)
    genre_id = Column(KeyType, ForeignKey("genres.id"))
    director_id = Column(KeyType, ForeignKey("directors.id"))
    # many to one
    genre = relationship("Genre", back_populates="movies", lazy="noload")
    # many to one
    director = relationship("Director", back_populates="movies", lazy="noload")

