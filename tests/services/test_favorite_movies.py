from unittest.mock import MagicMock
import pytest

from app.dao import FavouriteMovieDAO
from app.exceptions import ItemNotFound, BadRequestData
from app.dao.models import FavouriteMovies
from app.services import FavouriteMovieService


class TestFavouriteMoviesService:

    @pytest.fixture()
    def favorite_movies_dao_mock(self):

        favorite_movies = {
            (1, 4): FavouriteMovies(user_id=1, movie_id=4),
            (2, 3): FavouriteMovies(user_id=2, movie_id=3),
            (3, 2): FavouriteMovies(user_id=3, movie_id=2),
            (4, 1): FavouriteMovies(user_id=4, movie_id=1),
        }

        def create(model):
            pk = (model.user_id, model.movie_id)
            favorite_movies[pk] = model
            return model

        def delete(model):
            pk = (model.user_id, model.movie_id)
            del favorite_movies[pk]

        def by_user(user_id, page=None):
            return [
                favorite_movie for favorite_movie in favorite_movies.values()
                if favorite_movie.user_id == user_id
            ]

        def by_movie(movie_id, page=None):
            return [
                favorite_movie for favorite_movie in favorite_movies.values()
                if favorite_movie.movie_id == movie_id
            ]


        dao = FavouriteMovieDAO(None)

        dao.get_by_id = MagicMock(side_effect=favorite_movies.get)
        dao.get_all = MagicMock(return_value=list(favorite_movies.items()))
        dao.create = MagicMock(side_effect=create)
        dao.update = dao.create
        dao.delete = MagicMock(side_effect=delete)
        dao.get_all_by_user_id = MagicMock(side_effect=by_user)
        dao.get_all_by_movie_id = MagicMock(side_effect=by_movie)

        return dao

    @pytest.fixture()
    def favorite_movies_service(self, favorite_movies_dao_mock):
        return FavouriteMovieService(dao=favorite_movies_dao_mock)

    def test_get_favorite_movie(self, favorite_movies_service):
        model = favorite_movies_service.get_item((1, 4, ))
        assert model
        assert model.user_id == 1
        assert model.movie_id == 4
        assert isinstance(model, FavouriteMovies)

    def test_favorite_movie_not_found(self, favorite_movies_dao_mock, favorite_movies_service):

        with pytest.raises(ItemNotFound):
            favorite_movies_service.get_item((10, 10, ))

    @pytest.mark.parametrize('page', [1, None], ids=['with page', 'without page'])
    def test_get_favorite_movies(self, favorite_movies_dao_mock, favorite_movies_service, page):
        favorite_movies = favorite_movies_service.get_all(page=page)
        assert len(favorite_movies) == 4
        assert favorite_movies == favorite_movies_dao_mock.get_all.return_value
        favorite_movies_dao_mock.get_all.assert_called_with(page=page)

    def test_create(self, favorite_movies_service):
        model = favorite_movies_service.create({"user_id": 99, "movie_id": 99})
        assert model
        assert favorite_movies_service.get_item((model.user_id, model.movie_id, ))
        assert favorite_movies_service.get_item((model.user_id, model.movie_id, )).user_id == 99
        assert favorite_movies_service.get_item((model.user_id, model.movie_id, )).movie_id == 99

    def test_create_bad_data(self, favorite_movies_service):
        with pytest.raises(BadRequestData):
            favorite_movies_service.create({"bad_key": "bad_value"})

    def test_update(self, favorite_movies_service):
        model = favorite_movies_service.update((1, 4, ), {"user_id": 1, "movie_id": 2})
        assert model
        assert model.movie_id == 2
        assert favorite_movies_service.get_item((1, 2, )).user_id == 1

    def test_update_bad_data(self, favorite_movies_service):
        with pytest.raises(BadRequestData):
            favorite_movies_service.update((1, 4), {"bad_key": "bad_value"})

    def test_partially_update(self, favorite_movies_service):
        model = favorite_movies_service.partially_update((1, 4,), {"movie_id": 2})
        assert model
        assert model.movie_id == 2
        assert favorite_movies_service.get_item((1, 2,)).movie_id == 2

    def test_partially_update_bad_data(self, favorite_movies_service):
        with pytest.raises(BadRequestData):
            favorite_movies_service.partially_update(1, {"bad_key": "bad_value"})

    def test_delete(self, favorite_movies_service):
        favorite_movies_service.delete((1, 4, ))
        with pytest.raises(ItemNotFound):
            favorite_movies_service.get_item((1, 4, ))

    def test_get_all_by_user_id(self, favorite_movies_service):
        models = favorite_movies_service.get_all_by_user_id(1)
        assert len(models) == 1
        assert models[0].movie_id == 4

    def test_get_all_by_movie_id(self, favorite_movies_service):
        models = favorite_movies_service.get_all_by_movie_id(1)
        assert len(models) == 1
        assert models[0].user_id == 4

