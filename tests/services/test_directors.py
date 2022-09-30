from unittest.mock import MagicMock
import pytest

from app.dao import DirectorDAO
from app.exceptions import ItemNotFound, BadRequestData
from app.dao.models import Director
from app.services import DirectorService


class TestDirectorsService:

    @pytest.fixture()
    def directors_dao_mock(self):

        directors = {
            1: Director(id=1, name='test_director_1'),
            2: Director(id=2, name='test_director_2'),
            3: Director(id=3, name='test_director_3'),
            4: Director(id=4, name='test_director_4'),
        }

        def create(model):
            model.id = max(directors.keys()) + 1
            directors[model.id] = model
            return model

        def delete(model):
            del directors[model.id]

        dao = DirectorDAO(None)

        dao.get_by_id = MagicMock(side_effect=directors.get)
        dao.get_all = MagicMock(return_value=list(directors.items()))
        dao.create = MagicMock(side_effect=create)
        dao.update = dao.create
        dao.delete = MagicMock(side_effect=delete)

        return dao

    @pytest.fixture()
    def directors_service(self, directors_dao_mock):
        return DirectorService(dao=directors_dao_mock)

    def test_get_director(self, directors_service):
        model = directors_service.get_item(1)
        assert model
        assert model.id == 1
        assert model.name == "test_director_1"
        assert isinstance(model, Director)

    def test_director_not_found(self, directors_dao_mock, directors_service):

        with pytest.raises(ItemNotFound):
            directors_service.get_item(10)

    @pytest.mark.parametrize('page', [1, None], ids=['with page', 'without page'])
    def test_get_directors(self, directors_dao_mock, directors_service, page):
        directors = directors_service.get_all(page=page)
        assert len(directors) == 4
        assert directors == directors_dao_mock.get_all.return_value
        directors_dao_mock.get_all.assert_called_with(page=page)

    def test_create(self, directors_service):
        model = directors_service.create({"name": "test_director_5"})
        assert model
        assert directors_service.get_item(model.id)
        assert directors_service.get_item(model.id).name == "test_director_5"

    def test_create_bad_data(self, directors_service):
        with pytest.raises(BadRequestData):
            directors_service.create({"bad_key": "bad_value"})

    def test_update(self, directors_service):
        model = directors_service.update(1, {"name": "test_update_name"})
        assert model
        assert model.name == "test_update_name"
        assert directors_service.get_item(1).name == "test_update_name"

    def test_update_bad_data(self, directors_service):
        with pytest.raises(BadRequestData):
            directors_service.update(1, {"bad_key": "bad_value"})

    def test_partially_update(self, directors_service):
        pass

    def test_partially_update_bad_data(self, directors_service):
        with pytest.raises(BadRequestData):
            directors_service.partially_update(1, {"bad_key": "bad_value"})

    def test_delete(self, directors_service):
        directors_service.delete(1)
        with pytest.raises(ItemNotFound):
            directors_service.get_item(1)

