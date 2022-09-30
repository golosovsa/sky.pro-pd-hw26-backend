from unittest.mock import MagicMock
import pytest

from app.dao import UserDAO
from app.exceptions import ItemNotFound, BadRequestData
from app.dao.models import User
from app.services import UserService
from app.tools.security import compose_passwords, generate_password_hash


class TestUsersService:

    @pytest.fixture()
    def users_dao_mock(self):
        users = {
            1: User(
                id=1,
                email="test_user_1_email",
                password='test_user_1_password',
                name='test_user_1_name',
                surname='test_user_1_surname',
                favourite_genre=1,
            ),
            2: User(
                id=2,
                email="test_user_2_email",
                password='test_user_2_password',
                name='test_user_2_name',
                surname='test_user_2_surname',
                favourite_genre=2,
            ),
            3: User(
                id=3,
                email="test_user_3_email",
                password='test_user_3_password',
                name='test_user_3_name',
                surname='test_user_3_surname',
                favourite_genre=3,
            ),
            4: User(
                id=4,
                email="test_user_4_email",
                password='test_user_4_password',
                name='test_user_4_name',
                surname='test_user_4_surname',
                favourite_genre=4,
            ),
        }

        def create(model):
            model.id = max(users.keys()) + 1
            users[model.id] = model
            return model

        def delete(model):
            del users[model.id]

        def by_email(email):
            for user in users.values():
                if user.email == email:
                    return user

        dao = UserDAO(None)

        dao.get_by_id = MagicMock(side_effect=users.get)
        dao.get_all = MagicMock(return_value=list(users.values()))
        dao.create = MagicMock(side_effect=create)
        dao.update = dao.create
        dao.delete = MagicMock(side_effect=delete)
        dao.get_by_email = MagicMock(side_effect=by_email)

        return dao

    @pytest.fixture()
    def users_service(self, users_dao_mock):
        return UserService(dao=users_dao_mock)

    def test_get_user(self, users_service):
        model = users_service.get_item(1)
        assert model
        assert model.id == 1
        assert model.email == "test_user_1_email"
        assert isinstance(model, User)

    def test_user_not_found(self, users_dao_mock, users_service):
        with pytest.raises(ItemNotFound):
            users_service.get_item(10)

    @pytest.mark.parametrize('page', [1, None], ids=['with page', 'without page'])
    def test_get_users(self, users_dao_mock, users_service, page):
        users = users_service.get_all(page=page)
        assert len(users) == 4
        assert users == users_dao_mock.get_all.return_value
        users_dao_mock.get_all.assert_called_with(page=page)

    def test_create(self, users_service):
        model = users_service.create(
            {
                "email": 'test_user_5_email',
                "password": 'test_user_5_password',
                "name": 'test_user_5_name',
                "surname": 'test_user_5_surname',
                "favourite_genre": 5,
            })
        assert model
        assert users_service.get_item(model.id)
        assert users_service.get_item(model.id).email == "test_user_5_email"

    def test_create_bad_data(self, users_service):
        with pytest.raises(BadRequestData):
            users_service.create({"bad_key": "bad_value"})

    def test_update(self, users_service):
        model = users_service.update(1, {
            "email": 'test_user_1_email_update',
            "password": 'test_user_1_password_update',
            "name": 'test_user_1_name_update',
            "surname": 'test_user_1_surname_update',
            "favourite_genre": 11,
        })
        assert model
        assert model.email == "test_user_1_email_update"
        assert users_service.get_item(1).email == "test_user_1_email_update"

    def test_update_bad_data(self, users_service):
        with pytest.raises(BadRequestData):
            users_service.update(1, {"bad_key": "bad_value"})

    def test_partially_update(self, users_service):
        model = users_service.partially_update(1, {
            "email": 'test_user_1_email_update',
        })
        assert model
        assert model.email == "test_user_1_email_update"
        assert users_service.get_item(1).email == "test_user_1_email_update"

    def test_partially_update_bad_data(self, users_service):
        with pytest.raises(BadRequestData):
            users_service.partially_update(1, {"bad_key": "bad_value"})

    def test_delete(self, users_service):
        users_service.delete(1)
        with pytest.raises(ItemNotFound):
            users_service.get_item(1)

    def test_calc_password_difficulty(self):
        assert UserService.calc_password_difficulty("") == 0
        assert UserService.calc_password_difficulty("1234567") == 1
        assert UserService.calc_password_difficulty("abcdefg") == 1
        assert UserService.calc_password_difficulty("!@#$%^&") == 1
        assert UserService.calc_password_difficulty("a1") == 2
        assert UserService.calc_password_difficulty("aA") == 2
        assert UserService.calc_password_difficulty("!A") == 2
        assert UserService.calc_password_difficulty("!1") == 2
        assert UserService.calc_password_difficulty("1aA!") == 4
        assert UserService.calc_password_difficulty("1aA!1234") == 5

    def test_create_tokens(self, app, users_service):
        user = users_service.get_item(1)
        tokens = users_service.create_tokens(user)
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert isinstance(tokens["access_token"], str)
        assert isinstance(tokens["refresh_token"], str)
        assert tokens["access_token"]
        assert tokens["refresh_token"]

    def test_register(self, app, users_service):
        data = {"email": "test_email", "password": "TEST_password_1!"}
        model = users_service.register(data)
        assert model
        assert model.password != "TEST_password_1!"

    def test_register_failed_empty_data(self, app, users_service):
        with pytest.raises(BadRequestData):
            users_service.register({})
        with pytest.raises(BadRequestData):
            users_service.register({"email": "email"})
        with pytest.raises(BadRequestData):
            users_service.register({"password": "TEST_password_1!"})

    def test_register_low_difficulty(self, app, users_service):
        with pytest.raises(BadRequestData):
            users_service.register({
                "email": "email",
                "password": ""
            })
        with pytest.raises(BadRequestData):
            users_service.register({
                "email": "email",
                "password": "qwerty"
            })
        with pytest.raises(BadRequestData):
            users_service.register({
                "email": "email",
                "password": "12345"
            })

    def test_user_login(self, app, users_service):
        data = {"email": "test_email", "password": "TEST_password_1!"}
        model = users_service.register(data)
        tokens = users_service.login({"email": "test_email", "password": "TEST_password_1!"})
        assert tokens
        assert "access_token" in tokens
        assert "refresh_token" in tokens

    def test_user_login_failed_wrong_data(self, app, users_service):
        with pytest.raises(BadRequestData):
            users_service.login({})
            users_service.login({"email": "email"})
            users_service.login({"password": "TEST_password_1!"})

    def test_user_login_failed_wrong_user(self, app, users_service):
        with pytest.raises(BadRequestData):
            users_service.login({"email": "_wrong_", "password": "TEST_password_1!"})

    def test_user_login_failed_wrong_password(self, app, users_service):
        with pytest.raises(BadRequestData):
            users_service.login({"email": "test_user_1_email", "password": "_wrong_"})

    def test_refresh(self, app, users_service):
        data = {"email": "test_email", "password": "TEST_password_1!"}
        model = users_service.register(data)
        tokens = users_service.login({"email": "test_email", "password": "TEST_password_1!"})

        refreshed_tokens = users_service.refresh(tokens["refresh_token"])

        assert refreshed_tokens
        assert "access_token" in refreshed_tokens
        assert "refresh_token" in refreshed_tokens

    def test_get(self, users_service):
        data = {"id": 1, "email": "test_user_1_email", "exp": "123"}
        model = users_service.get(data)
        assert model

    def test_get_failed(self, users_service):
        with pytest.raises(BadRequestData):
            model = users_service.get({})
        with pytest.raises(BadRequestData):
            model = users_service.get({"id": 1})
        with pytest.raises(BadRequestData):
            model = users_service.get({"id": 1, "email": "test_user_1_email"})
        with pytest.raises(BadRequestData):
            model = users_service.get({"id": 1, "email": "_wrong_", "exp": "123"})

    def test_patch(self, users_service):
        token_data = {"id": 1, "email": "test_user_1_email", "exp": "123"}
        data = {"name": "test_name"}
        model = users_service.patch(token_data, data)

        assert model
        assert model.name == "test_name"

    def test_patch_failed(self, users_service):
        token_data = {"id": 1, "email": "test_user_1_email", "exp": "123"}
        data = {"password": "test_password"}
        with pytest.raises(BadRequestData):
            model = users_service.patch(token_data, data)
        data = {"email": "test_new_email"}
        with pytest.raises(BadRequestData):
            model = users_service.patch(token_data, data)

    def test_set_password(self, app, users_service):
        data = {"email": "new_email", "password": "NEW_passwd_123!"}
        model = users_service.register(data)
        token_data = {
            "id": model.id,
            "email": model.email,
            "exp": 123,
        }
        data = {
            "old_password": "NEW_passwd_123!",
            "new_password": "NEW_NEW_passwd_123!",
        }
        model = users_service.set_password(token_data, data)

        assert model
        assert compose_passwords(
            generate_password_hash(data["new_password"]),
            model.password
        )

