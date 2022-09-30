"""
    Genre sqlalchemy model
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.setup.db.models import BaseWithID, db


class Genre(BaseWithID):
    __tablename__ = 'genres'

    name = Column(String(100), unique=True, nullable=False)
    # one to many
    movies = relationship("Movie", back_populates="genre", lazy="noload")

