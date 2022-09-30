import pytest
from sqlalchemy.exc import IntegrityError

from app.dao import DirectorDAO
from app.dao.models import Director


class TestDirectorsDAO:

    @pytest.fixture()
    def directors_dao(self, db):
        return DirectorDAO(db.session)

    @pytest.fixture()
    def director_1(self, db):
        model = Director(name="Никита Сергеевич Михалков")
        db.session.add(model)
        db.session.commit()
        return model

    @pytest.fixture()
    def director_2(self, db):
        model = Director(name="Тимур Нуруахитович Бекмамбетов")
        db.session.add(model)
        db.session.commit()
        return model

    def test_get_director_by_id(self, director_1, directors_dao):
        assert directors_dao.get_by_id(director_1.id) == director_1

    def test_get_director_by_id_not_found(self, directors_dao):
        assert not directors_dao.get_by_id(1)

    def test_get_all_directors(self, directors_dao, director_1, director_2):
        assert directors_dao.get_all() == [director_1, director_2]

    def test_get_director_by_page(self, app, directors_dao, director_1, director_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert directors_dao.get_all(page=1) == [director_1]
        assert directors_dao.get_all(page=2) == [director_2]
        assert directors_dao.get_all(page=3) == []

    def test_director_updatable_fields(self, directors_dao):
        assert "name" in directors_dao.__updatable_fields__

    def test_director_create(self, directors_dao):
        director = Director(name="test_create_genre")
        directors_dao.create(director)
        assert directors_dao.get_by_id(director.id) == director

    def test_director_create_uniq(self, directors_dao, director_1):
        model = Director(name="Никита Сергеевич Михалков")
        with pytest.raises(IntegrityError):
            directors_dao.create(model)

    def test_director_delete(self, directors_dao, director_1):
        pk = director_1.id
        directors_dao.delete(director_1)
        assert directors_dao.get_by_id(pk) is None

    def test_director_update(self, directors_dao, director_1):
        director_1.name = "test_update_director"
        directors_dao.update(director_1)
        assert directors_dao.get_by_id(director_1.id).name == "test_update_director"

    def test_director_update_uniq(self, directors_dao, director_1, director_2):
        director_1.name = "Тимур Нуруахитович Бекмамбетов"
        with pytest.raises(IntegrityError):
            directors_dao.update(director_1)
