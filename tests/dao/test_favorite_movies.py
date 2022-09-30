import pytest
from sqlalchemy.exc import IntegrityError

from app.dao import FavouriteMovieDAO
from app.dao.models import FavouriteMovies


class TestFavoriteMoviesDAO:

    @pytest.fixture()
    def favorite_movies_dao(self, db):
        return FavouriteMovieDAO(db.session)

    @pytest.fixture()
    def favorite_movie_1(self, db):
        model = FavouriteMovies(user_id=1, movie_id=2)
        db.session.add(model)
        db.session.commit()
        return model

    @pytest.fixture()
    def favorite_movie_2(self, db):
        model = FavouriteMovies(user_id=1, movie_id=1)
        db.session.add(model)
        db.session.commit()
        return model

    @pytest.fixture()
    def favorite_movie_3(self, db):
        model = FavouriteMovies(user_id=2, movie_id=3)
        db.session.add(model)
        db.session.commit()
        return model

    @pytest.fixture()
    def favorite_movie_4(self, db):
        model = FavouriteMovies(user_id=2, movie_id=1)
        db.session.add(model)
        db.session.commit()
        return model

    def test_get_all_favorite_movies(
            self,
            favorite_movies_dao,
            favorite_movie_1,
            favorite_movie_2,
            favorite_movie_3,
            favorite_movie_4
    ):
        assert favorite_movies_dao.get_all() == [
            favorite_movie_1,
            favorite_movie_2,
            favorite_movie_3,
            favorite_movie_4,
        ]

    def test_get_favorite_movie_by_page(self, app, favorite_movies_dao, favorite_movie_1, favorite_movie_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert favorite_movies_dao.get_all(page=1) == [favorite_movie_1]
        assert favorite_movies_dao.get_all(page=2) == [favorite_movie_2]
        assert favorite_movies_dao.get_all(page=5) == []

    def test_favorite_movie_updatable_fields(self, favorite_movies_dao):
        assert "user_id" in favorite_movies_dao.__updatable_fields__
        assert "movie_id" in favorite_movies_dao.__updatable_fields__

    def test_favorite_movie_create(self, favorite_movies_dao):
        favorite_movie = FavouriteMovies(user_id=99, movie_id=99)
        favorite_movies_dao.create(favorite_movie)
        assert favorite_movies_dao.get_by_ids(favorite_movie.user_id, favorite_movie.movie_id) == favorite_movie

    @pytest.mark.filterwarnings("ignore::sqlalchemy.exc.SAWarning")
    def test_favorite_movie_create_uniq(self, favorite_movies_dao, favorite_movie_1):
        model = FavouriteMovies(user_id=1, movie_id=2)
        with pytest.raises(IntegrityError):
            favorite_movies_dao.create(model)

    def test_favorite_movie_delete(self, favorite_movies_dao, favorite_movie_1):
        user_id, movie_id = favorite_movie_1.user_id, favorite_movie_1.movie_id
        favorite_movies_dao.delete(favorite_movie_1)
        assert favorite_movies_dao.get_by_ids(user_id, movie_id) is None

    def test_favorite_movie_update(self, favorite_movies_dao, favorite_movie_1):
        favorite_movie_1.movie_id = 99
        favorite_movies_dao.update(favorite_movie_1)
        assert favorite_movies_dao.get_by_ids(
            favorite_movie_1.user_id,
            favorite_movie_1.movie_id,
        ).movie_id == 99

    @pytest.mark.filterwarnings("ignore::sqlalchemy.exc.SAWarning")
    def test_favorite_movie_update_uniq(self, favorite_movies_dao, favorite_movie_1, favorite_movie_2):
        favorite_movie_1.movie_id = 1
        with pytest.raises(IntegrityError):
            favorite_movies_dao.update(favorite_movie_1)

    def test_get_all_favorite_movies_by_user_id(
            self,
            favorite_movies_dao,
            favorite_movie_1,
            favorite_movie_2,
            favorite_movie_3,
            favorite_movie_4,
    ):
        models = favorite_movies_dao.get_all_by_user_id(1)
        assert models == [favorite_movie_2, favorite_movie_1]

    def test_get_all_favorite_movies_by_user_id_by_page(
            self,
            app,
            favorite_movies_dao,
            favorite_movie_1,
            favorite_movie_2,
            favorite_movie_3,
            favorite_movie_4,
    ):
        app.config['ITEMS_PER_PAGE'] = 1
        assert favorite_movies_dao.get_all_by_user_id(1, page=1) == [favorite_movie_2]
        assert favorite_movies_dao.get_all_by_user_id(1, page=2) == [favorite_movie_1]
        assert favorite_movies_dao.get_all_by_user_id(1, page=3) == []

    def test_get_all_favorite_movies_by_movie_id(
            self,
            favorite_movies_dao,
            favorite_movie_1,
            favorite_movie_2,
            favorite_movie_3,
            favorite_movie_4,
    ):
        models = favorite_movies_dao.get_all_by_movie_id(1)
        assert models == [favorite_movie_2, favorite_movie_4]

    def test_get_all_favorite_movies_by_movie_id_by_page(
            self,
            app,
            favorite_movies_dao,
            favorite_movie_1,
            favorite_movie_2,
            favorite_movie_3,
            favorite_movie_4,
    ):
        app.config['ITEMS_PER_PAGE'] = 1
        assert favorite_movies_dao.get_all_by_movie_id(1, page=1) == [favorite_movie_2]
        assert favorite_movies_dao.get_all_by_movie_id(1, page=2) == [favorite_movie_4]
        assert favorite_movies_dao.get_all_by_movie_id(1, page=3) == []

    def test_get_favorite_movie_by_ids(
            self,
            favorite_movies_dao,
            favorite_movie_1,
    ):
        model = favorite_movies_dao.get_by_ids(
            favorite_movie_1.user_id,
            favorite_movie_1.movie_id
        )

        assert model == favorite_movie_1
