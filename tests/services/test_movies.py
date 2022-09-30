from unittest.mock import MagicMock
import pytest

from app.dao import MovieDAO
from app.exceptions import ItemNotFound, BadRequestData
from app.dao.models import Movie
from app.services import MovieService


class TestMoviesService:

    @pytest.fixture()
    def movies_dao_mock(self):
        movies = {
            1: Movie(
                id=1,
                title='test_movie_1_title',
                description='test_movie_1_description',
                trailer='test_movie_1_trailer',
                year=2000,
                rating=8.0,
                genre_id=1,
                director_id=1,
            ),
            2: Movie(
                id=2,
                title='test_movie_2_title',
                description='test_movie_2_description',
                trailer='test_movie_2_trailer',
                year=2002,
                rating=8.2,
                genre_id=1,
                director_id=2,
            ),
            3: Movie(
                id=3,
                title='test_movie_3_title',
                description='test_movie_3_description',
                trailer='test_movie_3_trailer',
                year=2003,
                rating=8.3,
                genre_id=3,
                director_id=2,
            ),
            4: Movie(
                id=4,
                title='test_movie_4_title',
                description='test_movie_4_description',
                trailer='test_movie_4_trailer',
                year=2004,
                rating=8.4,
                genre_id=2,
                director_id=1,
            ),
        }

        def create(model):
            model.id = max(movies.keys()) + 1
            movies[model.id] = model
            return model

        def delete(model):
            del movies[model.id]

        dao = MovieDAO(None)

        dao.get_by_id = MagicMock(side_effect=movies.get)
        dao.get_all = MagicMock(return_value=list(movies.values()))
        dao.create = MagicMock(side_effect=create)
        dao.update = dao.create
        dao.delete = MagicMock(side_effect=delete)
        dao.get_all_and_order_by_newest = MagicMock(return_value=list(movies.values()))

        return dao

    @pytest.fixture()
    def movies_service(self, movies_dao_mock):
        return MovieService(dao=movies_dao_mock)

    def test_get_movie(self, movies_service):
        model = movies_service.get_item(1)
        assert model
        assert model.id == 1
        assert model.title == "test_movie_1_title"
        assert isinstance(model, Movie)

    def test_movie_not_found(self, movies_dao_mock, movies_service):
        with pytest.raises(ItemNotFound):
            movies_service.get_item(10)

    @pytest.mark.parametrize('page', [1, None], ids=['with page', 'without page'])
    def test_get_movies(self, movies_dao_mock, movies_service, page):
        movies = movies_service.get_all(page=page)
        assert len(movies) == 4
        assert movies == movies_dao_mock.get_all.return_value
        movies_dao_mock.get_all.assert_called_with(page=page)

    def test_create(self, movies_service):
        model = movies_service.create(
            {
                "title": 'test_movie_5_title',
                "description": 'test_movie_5_description',
                "trailer": 'test_movie_5_trailer',
                "year": 2005,
                "rating": 8.5,
                "genre_id": 99,
                "director_id": 99,
            })
        assert model
        assert movies_service.get_item(model.id)
        assert movies_service.get_item(model.id).title == "test_movie_5_title"

    def test_create_bad_data(self, movies_service):
        with pytest.raises(BadRequestData):
            movies_service.create({"bad_key": "bad_value"})

    def test_update(self, movies_service):
        model = movies_service.update(1, {
            "title": 'test_update_title',
            "description": 'test_movie_5_description',
            "trailer": 'test_movie_5_trailer',
            "year": 2005,
            "rating": 8.5,
            "genre_id": 99,
            "director_id": 99,
        })
        assert model
        assert model.title == "test_update_title"
        assert movies_service.get_item(1).title == "test_update_title"

    def test_update_bad_data(self, movies_service):
        with pytest.raises(BadRequestData):
            movies_service.update(1, {"bad_key": "bad_value"})

    def test_partially_update(self, movies_service):
        model = movies_service.partially_update(1, {
            "title": 'test_update_title',
        })
        assert model
        assert model.title == "test_update_title"
        assert movies_service.get_item(1).title == "test_update_title"

    def test_partially_update_bad_data(self, movies_service):
        with pytest.raises(BadRequestData):
            movies_service.partially_update(1, {"bad_key": "bad_value"})

    def test_delete(self, movies_service):
        movies_service.delete(1)
        with pytest.raises(ItemNotFound):
            movies_service.get_item(1)

    def test_get_all_with_status(self, movies_service):
        models = movies_service.get_all(status="new")
        assert models

    def test_get_all_with_wrong_status(self, movies_service):
        with pytest.raises(BadRequestData):
            movies_service.get_all(status="wrong_status")
