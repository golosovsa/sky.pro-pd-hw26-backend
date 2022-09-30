"""
    DAO abstraction level
    User DAO class
"""

from flask_sqlalchemy import BaseQuery

from .base import BaseDAO
from .models import User


class UserDAO(BaseDAO[User]):
    __model__ = User
    __updatable_fields__ = [
        "email",
        "password",
        "name",
        "surname",
        "favourite_genre",
    ]

    def get_by_email(self, email: str) -> User:
        query: BaseQuery = self._db_session.query(self.__model__)
        query = query.filter(User.email == email)
        return query.one_or_none()
