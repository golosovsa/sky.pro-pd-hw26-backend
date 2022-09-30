from typing import Generic, List, Optional, TypeVar

from flask import current_app
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import NotFound
from app.setup.db.models import Base

T = TypeVar('T', bound=Base)


class BaseDAO(Generic[T]):
    __model__ = Base
    __updatable_fields__ = []

    def __init__(self, db_session: scoped_session) -> None:
        self._db_session = db_session

    @property
    def _items_per_page(self) -> int:
        return current_app.config['ITEMS_PER_PAGE']

    def check_partially_data(self, data: dict) -> bool:
        """ Check data for unknown fields """
        for field in data:
            if field not in self.__updatable_fields__:
                return False
        return True

    def check_data(self, data: dict) -> bool:
        """ Check data for unknown fields and not enough fields """
        return self.check_partially_data(data) and len(data) == len(self.__updatable_fields__)

    def get_by_id(self, pk: int or tuple) -> Optional[T]:
        """ Get model by pk """
        return self._db_session.query(self.__model__).get(pk)

    def get_all(self, page: Optional[int] = None) -> List[T]:
        """ Get all models or by page """
        stmt: BaseQuery = self._db_session.query(self.__model__)
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()

    def create(self, model: Base):
        """ Create model """
        self._db_session.add(model)
        self._db_session.commit()
        return model

    update = create
    update.__doc__ = "Update model"

    def delete(self, model: Base):
        """ Delete model """
        self._db_session.delete(model)
        self._db_session.commit()
