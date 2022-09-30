import pytest
from sqlalchemy.exc import IntegrityError

from app.dao import GenreDAO
from app.dao.models import Genre


class TestGenresDAO:

    @pytest.fixture()
    def genres_dao(self, db):
        return GenreDAO(db.session)

    @pytest.fixture()
    def genre_1(self, db):
        model = Genre(name="Боевик")
        db.session.add(model)
        db.session.commit()
        return model

    @pytest.fixture()
    def genre_2(self, db):
        model = Genre(name="Комедия")
        db.session.add(model)
        db.session.commit()
        return model

    def test_get_genre_by_id(self, genre_1, genres_dao):
        assert genres_dao.get_by_id(genre_1.id) == genre_1

    def test_get_genre_by_id_not_found(self, genres_dao):
        assert not genres_dao.get_by_id(1)

    def test_get_all_genres(self, genres_dao, genre_1, genre_2):
        assert genres_dao.get_all() == [genre_1, genre_2]

    def test_get_genres_by_page(self, app, genres_dao, genre_1, genre_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert genres_dao.get_all(page=1) == [genre_1]
        assert genres_dao.get_all(page=2) == [genre_2]
        assert genres_dao.get_all(page=3) == []

    def test_genre_updatable_fields(self, genres_dao):
        assert "name" in genres_dao.__updatable_fields__

    def test_genre_create(self, genres_dao):
        genre = Genre(name="test_create_genre")
        genres_dao.create(genre)
        assert genres_dao.get_by_id(genre.id) == genre

    def test_genre_create_uniq(self, genres_dao, genre_1):
        model = Genre(name="Боевик")
        with pytest.raises(IntegrityError):
            genres_dao.create(model)

    def test_genre_delete(self, genres_dao, genre_1):
        pk = genre_1.id
        genres_dao.delete(genre_1)
        assert genres_dao.get_by_id(pk) is None

    def test_genre_update(self, genres_dao, genre_1):
        genre_1.name = "test_update_genre"
        genres_dao.update(genre_1)
        assert genres_dao.get_by_id(genre_1.id).name == "test_update_genre"

    def test_genre_update_uniq(self, genres_dao, genre_1, genre_2):
        genre_1.name = "Комедия"
        with pytest.raises(IntegrityError):
            genres_dao.update(genre_1)
