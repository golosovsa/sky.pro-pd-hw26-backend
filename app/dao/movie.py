"""
    DAO abstraction level
    Movie DAO class
"""
from typing import Optional, List
from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc
from werkzeug.exceptions import NotFound

from .base import BaseDAO
from .models import Movie


class MovieDAO(BaseDAO[Movie]):
    __model__ = Movie
    __updatable_fields__ = [
        "title",
        "description",
        "trailer",
        "year",
        "rating",
        "genre_id",
        "director_id",
    ]

    def get_all_and_order_by_newest(self, page: Optional[int] = None) -> List[Movie]:
        """ Get all models or by page and order by newest """
        stmt: BaseQuery = self._db_session.query(self.__model__)
        stmt = stmt.order_by(desc(Movie.created))
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()
