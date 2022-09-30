from sqlalchemy.exc import IntegrityError
import pytest

from app.dao import UserDAO
from app.dao.models import User


class TestUsersDAO:

    @pytest.fixture()
    def users_dao(self, db):
        return UserDAO(db.session)

    @pytest.fixture()
    def user_1(self, db):
        model = User(
            email="User_1",
            password="User_1_password",
            name="User_1",
            surname="User_1",
            favourite_genre=1,
        )
        db.session.add(model)
        db.session.commit()
        return model

    @pytest.fixture()
    def user_2(self, db):
        model = User(
            email="User_2",
            password="User_2_password",
            name="User_2",
            surname="User_2",
            favourite_genre=2,
        )
        db.session.add(model)
        db.session.commit()
        return model

    def test_get_user_by_id(self, user_1, users_dao):
        assert users_dao.get_by_id(user_1.id) == user_1

    def test_get_user_by_id_not_found(self, users_dao):
        assert not users_dao.get_by_id(1)

    def test_get_all_users(self, users_dao, user_1, user_2):
        assert users_dao.get_all() == [user_1, user_2]

    def test_get_users_by_page(self, app, users_dao, user_1, user_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert users_dao.get_all(page=1) == [user_1]
        assert users_dao.get_all(page=2) == [user_2]
        assert users_dao.get_all(page=3) == []

    def test_users_updatable_fields(self, users_dao):
        assert "email" in users_dao.__updatable_fields__
        assert "password" in users_dao.__updatable_fields__
        assert "name" in users_dao.__updatable_fields__
        assert "surname" in users_dao.__updatable_fields__
        assert "favourite_genre" in users_dao.__updatable_fields__

    def test_users_create(self, users_dao):
        user = User(
            email="User_test",
            password="User_test_password",
            name="User_test",
            surname="User_test",
            favourite_genre=2,
        )
        users_dao.create(user)
        assert users_dao.get_by_id(user.id) == user

    def test_user_create_uniq(self, users_dao, user_1):
        user = User(
            email="User_1",
            password="User_test_password",
            name="User_test",
            surname="User_test",
            favourite_genre=999,
        )
        with pytest.raises(IntegrityError):
            users_dao.create(user)

    def test_users_delete(self, users_dao, user_1):
        pk = user_1.id
        users_dao.delete(user_1)
        assert users_dao.get_by_id(pk) is None

    def test_users_update(self, users_dao, user_1):
        user_1.email = "test_update_user"
        user_1.password = "test_update_user"
        user_1.name = "test_update_user"
        user_1.surname = "test_update_user"
        user_1.favourite_genre = 999

        users_dao.update(user_1)

        user = users_dao.get_by_id(user_1.id)

        assert user.email == "test_update_user"
        assert user.password == "test_update_user"
        assert user.name == "test_update_user"
        assert user.surname == "test_update_user"
        assert user.favourite_genre == 999

    def test_users_update_uniq(self, users_dao, user_1, user_2):
        user_1.email = "User_2"
        with pytest.raises(IntegrityError):
            users_dao.update(user_1)

    def test_users_get_by_email(self, users_dao, user_1, user_2):
        model_1 = users_dao.get_by_email("User_1")
        model_2 = users_dao.get_by_email("User_2")
        assert model_1 == user_1
        assert model_2 == user_2
