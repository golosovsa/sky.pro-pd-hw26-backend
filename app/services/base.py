"""
    Service abstraction level
    Base service class
"""

from typing import Optional, List, TypeVar, Generic, Tuple
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.dao.base import BaseDAO
from app.exceptions import ItemNotFound, BadRequestData, BaseServiceError
from app.setup.db import Base

T = TypeVar("T", bound=BaseDAO)


class BaseService(Generic[T]):
    def __init__(self, dao: T):
        self._dao = dao

    def get_item(self, pk: int or Tuple[int, int]) -> Base:
        """ Get one model """
        if genre := self._dao.get_by_id(pk):
            return genre
        raise ItemNotFound(f'Genre with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> List[Base]:
        """ Get list of models """
        return self._dao.get_all(page=page)

    def create(self, data: dict) -> Base:
        """ Create model """
        if not self._dao.check_data(data):
            raise BadRequestData()
        try:
            return self._dao.create(self._dao.__model__(**data))

        except IntegrityError as e:
            if "UNIQUE constraint failed: users.email" in str(e):
                raise BadRequestData("A user with the same email address already exists")
            raise BaseServiceError("Something went wrong")
        except SQLAlchemyError:
            raise BaseServiceError()

    def update(self, pk: int or tuple, data: dict) -> Base:
        """ Update model """
        if not self._dao.check_data(data):
            raise BadRequestData()

        model = self.get_item(pk)
        for field in self._dao.__updatable_fields__:
            setattr(model, field, data.get(field))

        return self._dao.create(model)

    def partially_update(self, pk: int, data: dict) -> Base:
        """ Partially update model """
        if not self._dao.check_partially_data(data):
            raise BadRequestData

        model = self.get_item(pk)
        for field in self._dao.__updatable_fields__:
            if field in data:
                setattr(model, field, data.get(field))

        return self._dao.update(model)

    def delete(self, pk):
        """ Delete model """
        model = self._dao.get_by_id(pk)
        self._dao.delete(model)
