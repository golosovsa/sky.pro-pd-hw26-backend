from unittest.mock import MagicMock

import pytest

from app.dao import GenreDAO
from app.exceptions import ItemNotFound, BadRequestData
from app.dao.models import Genre
from app.services import GenreService


class TestGenresService:

    @pytest.fixture()
    def genres_dao_mock(self):

        genres = {
            1: Genre(id=1, name='test_genre_1'),
            2: Genre(id=2, name='test_genre_2'),
            3: Genre(id=3, name='test_genre_3'),
            4: Genre(id=4, name='test_genre_4'),
        }

        def create(model):
            model.id = max(genres.keys()) + 1
            genres[model.id] = model
            return model

        def delete(model):
            del genres[model.id]

        dao = GenreDAO(None)

        dao.get_by_id = MagicMock(side_effect=genres.get)
        dao.get_all = MagicMock(return_value=list(genres.values()))
        dao.create = MagicMock(side_effect=create)
        dao.update = dao.create
        dao.delete = MagicMock(side_effect=delete)

        return dao

    @pytest.fixture()
    def genres_service(self, genres_dao_mock):
        return GenreService(dao=genres_dao_mock)

    def test_get_genre(self, genres_service):
        model = genres_service.get_item(1)
        assert model
        assert model.id == 1
        assert model.name == "test_genre_1"
        assert isinstance(model, Genre)

    def test_genre_not_found(self, genres_dao_mock, genres_service):

        with pytest.raises(ItemNotFound):
            genres_service.get_item(10)

    @pytest.mark.parametrize('page', [1, None], ids=['with page', 'without page'])
    def test_get_genres(self, genres_dao_mock, genres_service, page):
        genres = genres_service.get_all(page=page)
        assert len(genres) == 4
        assert genres == genres_dao_mock.get_all.return_value
        genres_dao_mock.get_all.assert_called_with(page=page)

    def test_create(self, genres_service):
        model = genres_service.create({"name": "test_genre_5"})
        assert model
        assert genres_service.get_item(model.id)
        assert genres_service.get_item(model.id).name == "test_genre_5"

    def test_create_bad_data(self, genres_service):
        with pytest.raises(BadRequestData):
            genres_service.create({"bad_key": "bad_value"})

    def test_update(self, genres_service):
        model = genres_service.update(1, {"name": "test_update_name"})
        assert model
        assert model.name == "test_update_name"
        assert genres_service.get_item(1).name == "test_update_name"

    def test_update_bad_data(self, genres_service):
        with pytest.raises(BadRequestData):
            genres_service.update(1, {"bad_key": "bad_value"})

    def test_partially_update(self, genres_service):
        pass

    def test_partially_update_bad_data(self, genres_service):
        with pytest.raises(BadRequestData):
            genres_service.partially_update(1, {"bad_key": "bad_value"})

    def test_delete(self, genres_service):
        genres_service.delete(1)
        with pytest.raises(ItemNotFound):
            genres_service.get_item(1)
