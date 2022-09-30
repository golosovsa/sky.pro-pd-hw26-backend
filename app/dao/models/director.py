"""
    Director sqlalchemy model
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.setup.db.models import BaseWithID


class Director(BaseWithID):
    __tablename__ = 'directors'

    name = Column(String(100), unique=True, nullable=False)
    # one to many
    movies = relationship("Movie", back_populates="director", lazy="noload")
